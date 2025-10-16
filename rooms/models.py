from django.db import models


class Room(models.Model):
    """
    Room model representing the 15 total rooms in the workspace.
    - 8 Private Rooms (capacity 1)
    - 4 Conference Rooms (capacity varies, requires teams of 3+)
    - 3 Shared Desks (capacity 4 each)
    """
    
    ROOM_TYPES = [
        ('PRIVATE', 'Private Room'),
        ('CONFERENCE', 'Conference Room'),
        ('SHARED', 'Shared Desk'),
    ]
    
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['room_number']
    
    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"
    
    @property
    def is_private_room(self):
        return self.room_type == 'PRIVATE'
    
    @property
    def is_conference_room(self):
        return self.room_type == 'CONFERENCE'
    
    @property
    def is_shared_desk(self):
        return self.room_type == 'SHARED'
