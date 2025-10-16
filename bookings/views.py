from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Count
from datetime import datetime
from .models import Booking
from .serializers import (
    BookingCreateSerializer, 
    BookingSerializer, 
    BookingListSerializer
)
from rooms.models import Room
from rooms.serializers import RoomSerializer, RoomAvailabilitySerializer


class BookingCreateView(generics.CreateAPIView):
    """Create a new booking."""
    
    serializer_class = BookingCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Check room availability before creating booking
                room = serializer.validated_data['room']
                date = serializer.validated_data['date']
                start_time = serializer.validated_data['start_time']
                end_time = serializer.validated_data['end_time']
                
                # Check availability
                if not self.is_room_available(room, date, start_time, end_time):
                    return Response(
                        {"error": "No available room for the selected slot and type."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # For shared desks, check capacity
                if room.is_shared_desk:
                    current_occupancy = self.get_shared_desk_occupancy(room, date, start_time, end_time)
                    if current_occupancy >= room.capacity:
                        return Response(
                            {"error": "Shared desk is full for the selected time slot."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                booking = serializer.save()
                response_serializer = BookingSerializer(booking)
                
                return Response(
                    {
                        "message": "Booking created successfully",
                        "booking": response_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
                
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def is_room_available(self, room, date, start_time, end_time):
        """Check if room is available for the given time slot."""
        overlapping_bookings = Booking.objects.filter(
            room=room,
            date=date,
            status='ACTIVE',
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        # For private and conference rooms, no overlapping bookings allowed
        if room.is_private_room or room.is_conference_room:
            return not overlapping_bookings.exists()
        
        # For shared desks, check capacity
        return True  # Capacity check is done separately
    
    def get_shared_desk_occupancy(self, room, date, start_time, end_time):
        """Get current occupancy for a shared desk in the given time slot."""
        overlapping_bookings = Booking.objects.filter(
            room=room,
            date=date,
            status='ACTIVE',
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        total_occupancy = 0
        for booking in overlapping_bookings:
            total_occupancy += booking.occupancy_count
        
        return total_occupancy


class BookingListView(generics.ListAPIView):
    """List all active bookings."""
    
    serializer_class = BookingListSerializer
    
    def get_queryset(self):
        queryset = Booking.objects.filter(status='ACTIVE').select_related(
            'room', 'user', 'team'
        )
        
        # Filter by date if provided
        date = self.request.query_params.get('date')
        if date:
            try:
                parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=parsed_date)
            except ValueError:
                pass
        
        # Filter by room type if provided
        room_type = self.request.query_params.get('room_type')
        if room_type:
            queryset = queryset.filter(room__room_type=room_type)
        
        return queryset


class BookingDetailView(generics.RetrieveAPIView):
    """Get booking details by booking ID."""
    
    serializer_class = BookingSerializer
    lookup_field = 'booking_id'
    
    def get_queryset(self):
        return Booking.objects.select_related('room', 'user', 'team')


@api_view(['POST'])
def cancel_booking(request, booking_id):
    """Cancel a booking."""
    try:
        booking = Booking.objects.get(booking_id=booking_id, status='ACTIVE')
        booking.cancel()
        
        serializer = BookingSerializer(booking)
        return Response(
            {
                "message": "Booking cancelled successfully",
                "booking": serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except Booking.DoesNotExist:
        return Response(
            {"error": "Active booking not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def available_rooms(request):
    """Get available rooms for a specific time slot."""
    serializer = RoomAvailabilitySerializer(data=request.query_params)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    date = serializer.validated_data['date']
    start_time = serializer.validated_data['start_time']
    end_time = serializer.validated_data['end_time']
    room_type = serializer.validated_data.get('room_type')
    
    # Get all active rooms
    rooms = Room.objects.filter(is_active=True)
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    available_rooms = []
    
    for room in rooms:
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=room,
            date=date,
            status='ACTIVE',
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if room.is_private_room or room.is_conference_room:
            # Private and conference rooms are available if no overlapping bookings
            if not overlapping_bookings.exists():
                available_rooms.append({
                    'room': RoomSerializer(room).data,
                    'available_capacity': room.capacity,
                    'current_occupancy': 0
                })
        
        elif room.is_shared_desk:
            # Shared desks are available if capacity allows
            current_occupancy = sum(booking.occupancy_count for booking in overlapping_bookings)
            available_capacity = room.capacity - current_occupancy
            
            if available_capacity > 0:
                available_rooms.append({
                    'room': RoomSerializer(room).data,
                    'available_capacity': available_capacity,
                    'current_occupancy': current_occupancy
                })
    
    return Response({
        'date': date,
        'time_slot': f"{start_time} - {end_time}",
        'available_rooms': available_rooms,
        'total_available': len(available_rooms)
    })
