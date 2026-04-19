from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Course(models.Model):
    LEVEL_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    instructor_bio = models.TextField(blank=True)
    instructor_photo = models.ImageField(upload_to='instructors/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    duration = models.CharField(max_length=50)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']


class CourseMaterial(models.Model):
    MATERIAL_TYPES = [('pdf', 'PDF'), ('video', 'Video Link'), ('doc', 'Document'), ('zip', 'ZIP File')]

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
