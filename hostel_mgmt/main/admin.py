from django.contrib import admin
from .models import Room, Booking ,UserProfile

class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('number',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('student__username', 'room__number')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_student', 'department', 'reg_no', 'roll_no', 'phone_number')


admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
