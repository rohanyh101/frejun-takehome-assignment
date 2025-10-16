from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""
    
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'room_type', 'room_type_display',
            'capacity', 'is_active'
        ]
        read_only_fields = ['id']


class RoomAvailabilitySerializer(serializers.Serializer):
    """Serializer for room availability queries."""
    
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    room_type = serializers.ChoiceField(
        choices=Room.ROOM_TYPES,
        required=False
    )
    
    def validate(self, data):
        """Validate time slot constraints."""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time.")
            
            # Validate business hours (9 AM - 6 PM)
            from datetime import time
            allowed_start = time(9, 0)
            allowed_end = time(18, 0)
            
            if start_time < allowed_start or end_time > allowed_end:
                raise serializers.ValidationError(
                    "Bookings are only allowed between 9 AM and 6 PM."
                )
        
        return data
