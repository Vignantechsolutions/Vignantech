from django.db import models
from django.contrib.auth.models import User
from payments.models import Enrollment
import uuid


class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    issued_date = models.DateField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"CERT-{str(self.certificate_id)[:8].upper()} - {self.student.get_full_name()}"

    class Meta:
        ordering = ['-issued_date']


class CustomCertificate(models.Model):
    CERT_TYPE_CHOICES = [
        ('completion',    'Project Completion'),
        ('internship',    'Internship'),
        ('participation', 'Participation'),
        ('excellence',    'Excellence'),
        ('appreciation',  'Appreciation'),
        ('training',      'Training'),
    ]

    cert_number      = models.CharField(max_length=30, unique=True, editable=False)
    recipient_name   = models.CharField(max_length=150)
    cert_type        = models.CharField(max_length=20, choices=CERT_TYPE_CHOICES, default='completion')
    program_name     = models.CharField(max_length=200, help_text='Project / Course / Program title')
    project_domain   = models.CharField(max_length=300, blank=True,
                           help_text='e.g. Artificial Intelligence / Machine Learning / Data Science')
    start_date       = models.DateField(null=True, blank=True)
    end_date         = models.DateField(null=True, blank=True)
    issued_date      = models.DateField()
    signatory_name   = models.CharField(max_length=100, default='Suresh Tammali')
    signatory_title  = models.CharField(max_length=100, default='Director')
    signatory_org    = models.CharField(max_length=100, default='Vignan Tech Solutions')
    extra_note       = models.CharField(max_length=300, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    created_by       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                           related_name='custom_certificates')

    def save(self, *args, **kwargs):
        if not self.cert_number:
            last = CustomCertificate.objects.order_by('-id').first()
            next_num = (last.id + 1) if last else 1
            self.cert_number = f'VTS15112025{next_num:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cert_number} — {self.recipient_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Custom Certificate'
        verbose_name_plural = 'Custom Certificates'
