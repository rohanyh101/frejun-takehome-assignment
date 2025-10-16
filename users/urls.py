from django.urls import path
from .views import UserListCreateView, TeamListCreateView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('teams/', TeamListCreateView.as_view(), name='team-list'),
]
