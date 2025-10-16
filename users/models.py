from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes additional fields for age and gender as required by the business rules.
    """
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def is_child(self):
        """Children are defined as users under 10 years old."""
        return self.age < 10


class Team(models.Model):
    """
    Team model for group bookings.
    Conference rooms require teams with 3+ members.
    """
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        """Total count of members in the team."""
        return self.members.count()
    
    @property
    def adult_member_count(self):
        """Count of adult members (excluding children under 10)."""
        return self.members.filter(age__gte=10).count()
    
    @property
    def child_member_count(self):
        """Count of child members (under 10 years old)."""
        return self.members.filter(age__lt=10).count()
        
    def is_eligible_for_conference_room(self):
        """Teams need 3+ members to book conference rooms."""
        return self.member_count >= 3
