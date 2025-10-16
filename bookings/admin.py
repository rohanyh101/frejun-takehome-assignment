from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_id', 'room', 'booker_name', 'booking_type', 
        'date', 'start_time', 'end_time', 'status', 'created_at'
    ]
    list_filter = ['status', 'date', 'room__room_type']
    search_fields = ['booking_id', 'user__username', 'team__name']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
