from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer


class RoomListView(generics.ListAPIView):
    """List all active rooms."""
    
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        queryset = Room.objects.filter(is_active=True)
        
        # Filter by room type if provided
        room_type = self.request.query_params.get('room_type')
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        
        return queryset