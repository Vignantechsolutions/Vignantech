from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register_view),
    path('auth/verify-otp/', views.verify_otp_view),
    path('auth/login/', views.login_view),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/forgot-password/', views.forgot_password_view),
    path('auth/reset-password/', views.reset_password_view),

    # User
    path('profile/', views.ProfileView.as_view()),
    path('dashboard/', views.dashboard_view),

    # Content
    path('home/', views.home_data_view),
    path('courses/', views.CourseListView.as_view()),
    path('courses/<slug:slug>/', views.CourseDetailView.as_view()),
    path('internships/', views.InternshipListView.as_view()),
    path('internships/<slug:slug>/', views.InternshipDetailView.as_view()),
    path('projects/', views.ProjectListView.as_view()),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view()),
    path('domains/', views.ProjectDomainListView.as_view()),
    path('testimonials/', views.TestimonialListView.as_view()),
    path('testimonials/submit/', views.submit_review_view),

    # Payments
    path('payments/initiate/', views.initiate_payment_view),
    path('payments/callback/', views.payment_callback_view),

    # Certificates
    path('certificates/verify/<uuid:cert_id>/', views.verify_certificate_view),
    path('certificates/download/<uuid:cert_id>/', views.download_certificate_view),

    # Contact
    path('contact/', views.contact_view),
]
