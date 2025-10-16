from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/list/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<str:booking_id>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('cancel/<str:booking_id>/', views.cancel_booking, name='booking-cancel'),
    path('rooms/available/', views.available_rooms, name='rooms-available'),
]
