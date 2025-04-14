from django.db import models
from django.contrib.auth.models import User

# models.py

from django.db import models

# models.py

class Room(models.Model):
    number = models.CharField(max_length=10)
    capacity = models.IntegerField(default=3)  # Max number of people in a room
    is_available = models.BooleanField(default=True)

    @property
    def current_capacity(self):
        return self.booking_set.count()  # Count the number of bookings for this room

    def allocate_room(self, student, transaction_id):
        # You can define this method to allocate the room to a student
        # Example logic for allocating the room
        if self.current_capacity < self.capacity:
            Booking.objects.create(
                student=student,
                room=self,
                transaction_id=transaction_id,
                payment_status='paid',
                checked_in=True,
            )
            # After allocation, mark the room as unavailable if needed
            if self.current_capacity >= self.capacity:
                self.is_available = False
                self.save()
            return True
        return False


    def deallocate_room(self):
        """Decrease current capacity and mark room as available if capacity goes down"""
        self.current_capacity -= 1
        if self.current_capacity < self.capacity:
            self.is_available = True  # Room becomes available again if under capacity
        self.save()



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_student = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True)
    reg_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    roll_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=50, default='unpaid')
    checked_in = models.BooleanField(default=False)  # Add checked_in field
    checked_in_at = models.DateTimeField(null=True, blank=True)  # Add checked_in_at field
    
    def __str__(self):
        return f"Booking {self.id} for {self.student.username}"