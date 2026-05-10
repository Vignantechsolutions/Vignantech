from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from courses.models import Course
from internships.models import Internship
from projects.models import Project


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'core:corporate_training',
                'internships:list', 'courses:list', 'projects:list', 'certificates:verify']

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('courses:detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class InternshipSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Internship.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('internships:detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('projects:detail', args=[obj.slug])
