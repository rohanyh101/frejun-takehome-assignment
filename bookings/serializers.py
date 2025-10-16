from rest_framework import serializers
from .models import Booking
from users.serializers import UserSerializer, TeamSerializer
from rooms.serializers import RoomSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings."""
    
    class Meta:
        model = Booking
        fields = [
            'room', 'date', 'start_time', 'end_time', 'user', 'team'
        ]
    
    def validate(self, data):
        """Validate booking constraints."""
        # Ensure either user or team is provided (but not both)
        user = data.get('user')
        team = data.get('team')
        
        if not user and not team:
            raise serializers.ValidationError("Either user or team must be provided.")
        
        if user and team:
            raise serializers.ValidationError("Cannot specify both user and team.")
        
        return data
    
    def create(self, validated_data):
        """Create booking with proper validation."""
        try:
            booking = Booking.objects.create(**validated_data)
            return booking
        except Exception as e:
            raise serializers.ValidationError(str(e))


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for displaying booking details."""
    
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    booking_type = serializers.ReadOnlyField()
    booker_name = serializers.ReadOnlyField()
    occupancy_count = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'room', 'date', 'start_time', 'end_time',
            'user', 'team', 'booking_type', 'booker_name', 'occupancy_count',
            'status', 'status_display', 'created_at', 'cancelled_at'
        ]
        read_only_fields = ['booking_id', 'created_at', 'cancelled_at']


class BookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for booking lists."""
    
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    room_type = serializers.CharField(source='room.get_room_type_display', read_only=True)
    booker_name = serializers.ReadOnlyField()
    booking_type = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'room_number', 'room_type', 'date', 
            'start_time', 'end_time', 'booker_name', 'booking_type',
            'status', 'status_display', 'created_at'
        ]
