from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time
from users.models import User, Team
from rooms.models import Room


class Booking(models.Model):
    """
    Booking model representing room reservations.
    Handles both individual and team bookings with proper constraints.
    """
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    
    # Booking identification
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Room and timing
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # User/Team information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='individual_bookings', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_bookings', null=True, blank=True)
    
    # Booking metadata
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', 'date', 'start_time']),
            models.Index(fields=['booking_id']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(team__isnull=False),
                name='booking_must_have_user_or_team'
            ),
            models.CheckConstraint(
                check=~(models.Q(user__isnull=False) & models.Q(team__isnull=False)),
                name='booking_cannot_have_both_user_and_team'
            ),
        ]
    
    def __str__(self):
        if self.team:
            return f"Team {self.team.name} - {self.room} on {self.date} ({self.start_time}-{self.end_time})"
        return f"{self.user} - {self.room} on {self.date} ({self.start_time}-{self.end_time})"
    
    def save(self, *args, **kwargs):
        # Generate unique booking ID if not exists
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        
        # Validate booking before saving
        self.clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate booking constraints and business rules."""
        errors = {}
        
        # Check that booking has either user or team (but not both)
        if not self.user and not self.team:
            errors['user'] = "Booking must have either a user or a team."
        
        if self.user and self.team:
            errors['user'] = "Booking cannot have both a user and a team."
        
        # Validate time slot constraints (9 AM - 6 PM)
        if not self.is_valid_time_slot():
            errors['start_time'] = "Bookings are only allowed between 9 AM and 6 PM."
        
        # Validate end time is after start time
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            errors['end_time'] = "End time must be after start time."
        
        # Validate room type constraints
        room_validation_error = self.validate_room_constraints()
        if room_validation_error:
            errors['room'] = room_validation_error
        
        # Check for overlapping bookings
        overlap_error = self.check_overlapping_bookings()
        if overlap_error:
            errors['start_time'] = overlap_error
        
        if errors:
            raise ValidationError(errors)
    
    def is_valid_time_slot(self):
        """Check if booking is within allowed hours (9 AM - 6 PM)."""
        if not self.start_time or not self.end_time:
            return False
        
        allowed_start = time(9, 0)  # 9 AM
        allowed_end = time(18, 0)   # 6 PM
        
        return (self.start_time >= allowed_start and 
                self.end_time <= allowed_end)
    
    def validate_room_constraints(self):
        """Validate room-specific booking constraints."""
        if not self.room:
            return None
        
        # Private room constraints
        if self.room.is_private_room:
            if self.team:
                return "Private rooms can only be booked by individual users."
        
        # Conference room constraints
        elif self.room.is_conference_room:
            if self.user:
                return "Conference rooms can only be booked by teams with 3+ members."
            if self.team and not self.team.is_eligible_for_conference_room():
                return "Conference rooms require teams with at least 3 members."
        
        # Shared desk constraints are handled at the availability level
        return None
    
    def check_overlapping_bookings(self):
        """Check for time slot conflicts in the same room."""
        if not self.room or not self.date or not self.start_time or not self.end_time:
            return None
        
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            date=self.date,
            status='ACTIVE'
        ).exclude(pk=self.pk if self.pk else None)
        
        for booking in overlapping_bookings:
            if self.times_overlap(booking):
                return f"Time slot conflicts with existing booking {booking.booking_id}."
        
        return None
    
    def times_overlap(self, other_booking):
        """Check if two bookings have overlapping time slots."""
        return (self.start_time < other_booking.end_time and 
                self.end_time > other_booking.start_time)
    
    def generate_booking_id(self):
        """Generate a unique booking ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BK{timestamp}"
    
    def cancel(self):
        """Cancel the booking and update status."""
        self.status = 'CANCELLED'
        self.cancelled_at = timezone.now()
        self.save()
    
    @property
    def is_active(self):
        return self.status == 'ACTIVE'
    
    @property
    def is_cancelled(self):
        return self.status == 'CANCELLED'
    
    @property
    def booking_type(self):
        return 'Team' if self.team else 'Individual'
    
    @property
    def booker_name(self):
        if self.team:
            return self.team.name
        return str(self.user)
    
    @property
    def occupancy_count(self):
        """Return the number of people this booking accounts for."""
        if self.team:
            # Children are included in headcount but don't occupy seats
            return self.team.adult_member_count
        return 1 if not self.user.is_child else 0
