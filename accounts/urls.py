from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/verify/', views.verify_otp, name='verify_otp'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/verify/', views.verify_reset_otp, name='verify_reset_otp'),
    path('forgot-password/reset/', views.reset_password, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('assignment/<int:enrollment_id>/', views.submit_assignment, name='submit_assignment'),
    path('review/', views.submit_review, name='submit_review'),
]
