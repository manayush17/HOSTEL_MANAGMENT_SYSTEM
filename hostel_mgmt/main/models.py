from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Room {self.number}"


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
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='paid')

    def __str__(self):
        return f"{self.student.username} - {self.room.number}"
