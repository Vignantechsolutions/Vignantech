from django.db import models


class Internship(models.Model):
    MODE_CHOICES = [('online', 'Online'), ('offline', 'Offline'), ('hybrid', 'Hybrid')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    topics_covered = models.TextField(help_text='Enter topics separated by newlines')
    benefits = models.TextField(help_text='Enter benefits separated by newlines')
    certificate_info = models.TextField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')
    thumbnail = models.ImageField(upload_to='internships/', blank=True, null=True)
    seats_available = models.PositiveIntegerField(default=50)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_topics_list(self):
        return [t.strip() for t in self.topics_covered.split('\n') if t.strip()]

    def get_benefits_list(self):
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]

    class Meta:
        ordering = ['-created_at']
