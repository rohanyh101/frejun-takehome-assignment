from rest_framework import generics
from .models import User, Team
from .serializers import UserSerializer, TeamSerializer


class UserListCreateView(generics.ListCreateAPIView):
    """List and create users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamListCreateView(generics.ListCreateAPIView):
    """List and create teams."""
    queryset = Team.objects.all().prefetch_related('members')
    serializer_class = TeamSerializer
    
    def perform_create(self, serializer):
        # For now, we'll use the first user as creator
        # In a real app, this would be request.user
        first_user = User.objects.first()
        if first_user:
            serializer.save(created_by=first_user)
        else:
            # Create a default user if none exists
            default_user = User.objects.create_user(
                username='system',
                first_name='System',
                last_name='User',
                email='system@example.com',
                age=30,
                gender='O'
            )
            serializer.save(created_by=default_user)


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a team."""
    queryset = Team.objects.all().prefetch_related('members')
    serializer_class = TeamSerializer