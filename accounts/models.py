from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone
from datetime import timedelta


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200, blank=True)
    course_of_study = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'


class OTPVerification(models.Model):
    PURPOSE_REGISTER = 'register'
    PURPOSE_RESET = 'reset'
    PURPOSE_CHOICES = [
        (PURPOSE_REGISTER, 'Email Verification'),
        (PURPOSE_RESET, 'Password Reset'),
    ]

    email = models.EmailField()
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            from django.conf import settings
            minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
            self.expires_at = timezone.now() + timedelta(minutes=minutes)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate(cls, email, purpose):
        cls.objects.filter(email=email, purpose=purpose, is_verified=False).delete()
        otp = str(random.randint(100000, 999999))
        return cls.objects.create(email=email, otp=otp, purpose=purpose)

    def __str__(self):
        return f"{self.email} — {self.purpose} — {self.otp}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'


class Testimonial(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False, help_text='Approve to show on website')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.designation}"

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
