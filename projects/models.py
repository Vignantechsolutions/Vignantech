from django.db import models


class ProjectDomain(models.Model):
    name = models.CharField(max_length=100, help_text='e.g. AI & Machine Learning')
    slug = models.SlugField(unique=True, help_text='e.g. aiml — used in URLs and CSS classes')
    emoji = models.CharField(max_length=10, default='💻', help_text='Domain emoji shown on cards')
    color_from = models.CharField(max_length=7, default='#1E3A8A', help_text='Gradient start hex color')
    color_to = models.CharField(max_length=7, default='#3B82F6', help_text='Gradient end hex color')
    badge_bg = models.CharField(max_length=30, default='rgba(59,130,246,.12)', help_text='Badge background (CSS rgba)')
    badge_color = models.CharField(max_length=7, default='#1D4ED8', help_text='Badge text hex color')
    description = models.TextField(blank=True, help_text='Short description shown on listing page')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def gradient(self):
        return f'linear-gradient(135deg,{self.color_from},{self.color_to})'

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Project Domain'
        verbose_name_plural = 'Project Domains'


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    domain = models.ForeignKey(
        ProjectDomain, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projects', help_text='Select the project domain'
    )
    description = models.TextField()
    problem_statement = models.TextField(blank=True)
    objectives = models.TextField(blank=True, help_text='One objective per line')
    tech_stack = models.CharField(max_length=500)
    algorithms = models.TextField(blank=True, help_text='One algorithm per line')
    features = models.TextField(blank=True, help_text='One feature per line')
    dataset = models.CharField(max_length=300, blank=True)
    conclusion = models.TextField(blank=True)
    future_enhancements = models.TextField(blank=True, help_text='One enhancement per line')
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='projects/screenshots/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
