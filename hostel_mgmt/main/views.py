from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseForbidden

from .models import Room, Booking
from django.contrib.auth.models import User

def index(request):
    return render(request, 'main/index.html')


from .models import UserProfile  # Make sure this import is present

import re
from django.contrib import messages
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        is_student = 'is_student' in request.POST

        name = request.POST.get('name', '').strip()
        department = request.POST.get('department', '').strip()
        reg_no = request.POST.get('reg_no', '').strip()
        roll_no = request.POST.get('roll_no', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()

        # 📱 Phone validation
        if is_student and (not phone_number.isdigit() or len(phone_number) != 10):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, 'main/register.html')

        # 🧾 Required student fields
        if is_student and (not department or not reg_no or not roll_no):
            messages.error(request, "Please fill all required student details.")
            return render(request, 'main/register.html')

        # 🔑 Password length
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'main/register.html')

        # ❌ Check if username is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'main/register.html')

        # ✅ Create user
        user = User.objects.create_user(username=username, password=password)
        if name:
            user.first_name = name
        if not is_student:
            user.is_staff = True
        user.save()

        # ✅ Create profile
        if is_student:
            UserProfile.objects.create(
                user=user,
                is_student=True,
                department=department,
                reg_no=reg_no,
                roll_no=roll_no,
                phone_number=phone_number
            )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'main/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            return render(request, 'main/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.is_staff:
        # Admin dashboard: Show all bookings, allocated rooms, and free rooms
        bookings = Booking.objects.select_related('room', 'student')  # Fetch room and student info
        allocated_rooms = Room.objects.filter(is_available=False)
        free_rooms = Room.objects.filter(is_available=True)

        return render(request, 'main/admin_dashboard.html', {
            'bookings': bookings,
            'allocated_rooms': allocated_rooms,
            'free_rooms': free_rooms
        })
    else:
        # Student dashboard logic
        current_booking = Booking.objects.filter(student=request.user).select_related('room').first()

        # Get available rooms with less than 3 students already booked
        rooms = Room.objects.all()
        available_rooms = []

        for room in rooms:
            # Count the number of bookings for the room
            current_capacity = Booking.objects.filter(room=room).count()
            if current_capacity < 3:
                available_rooms.append(room)

        return render(request, 'main/student_dashboard.html', {
            'rooms': available_rooms,
            'current_booking': current_booking
        })

@csrf_protect
@login_required
def check_in(request, room_id):
    if request.user.is_staff:
        return HttpResponseForbidden("Admins cannot book rooms.")

    room = get_object_or_404(Room, id=room_id)

    # Calculate the current capacity
    current_capacity = room.current_capacity

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        if not transaction_id:
            return render(request, 'main/check_in.html', {
                'room': room,
                'error': 'Please enter a transaction ID.',
                'current_capacity': current_capacity
            })

        # Try to allocate the room
        if room.allocate_room(student=request.user, transaction_id=transaction_id):
            return redirect('dashboard')
        else:
            return render(request, 'main/check_in.html', {
                'room': room,
                'error': 'This room is full. Cannot book anymore students.',
                'current_capacity': current_capacity
            })

    # On GET request, display the room details
    return render(request, 'main/check_in.html', {'room': room, 'current_capacity': current_capacity})


@login_required
def check_out(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    room = booking.room

    # Delete booking record
    booking.delete()

    # Mark room as available
    room.is_available = True
    room.save()

    return redirect('dashboard')


@csrf_protect
@login_required
def add_room(request):
    # Only allow staff (admins) to add rooms
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to add rooms.")

    if request.method == 'POST':
        number = request.POST.get('number')
        if number:
            # Create a new room
            Room.objects.create(number=number, is_available=True)
            return redirect('dashboard')
    
    return render(request, 'main/add_room.html')


@login_required
def admin_deallocate(request, booking_id):
    # Only allow staff (admins) to deallocate rooms
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admins can perform this action.")

    # Get the booking and related room
    booking = get_object_or_404(Booking, id=booking_id)
    room = booking.room

    # Delete the booking and mark the room as available
    booking.delete()
    room.is_available = True
    room.save()

    return redirect('dashboard')
