from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView
from core.sitemaps import StaticViewSitemap

sitemaps = {'static': StaticViewSitemap}

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('internships/', include('internships.urls')),
    path('projects/', include('projects.urls')),
    path('payments/', include('payments.urls')),
    path('certificates/', include('certificates.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
