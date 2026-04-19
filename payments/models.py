from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from internships.models import Internship


class Enrollment(models.Model):
    TYPE_CHOICES = [('course', 'Course'), ('internship', 'Internship')]
    STATUS_CHOICES = [('pending', 'Pending'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    internship = models.ForeignKey(Internship, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        item = self.course or self.internship
        return f"{self.student.get_full_name()} - {item}"

    class Meta:
        ordering = ['-enrolled_at']


class Payment(models.Model):
    STATUS_CHOICES = [('created', 'Created'), ('paid', 'Paid'), ('failed', 'Failed'), ('refunded', 'Refunded')]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='payment')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='INR')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - ₹{self.amount} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class Assignment(models.Model):
    STATUS_CHOICES = [('submitted', 'Submitted'), ('reviewed', 'Reviewed'), ('approved', 'Approved')]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='assignments/')
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} - {self.title}"
