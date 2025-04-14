from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-room/', views.add_room, name='add_room'),
    path('check-in/<int:room_id>/', views.check_in, name='check_in'),
    path('check-out/<int:booking_id>/', views.check_out, name='check_out'),
    path('admin-deallocate/<int:booking_id>/', views.admin_deallocate, name='admin_deallocate'),

]
