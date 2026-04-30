from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('download/<uuid:cert_id>/', views.download_certificate, name='download'),
    path('verify/', views.verify_certificate, name='verify'),
    path('verify/<uuid:cert_id>/', views.verify_certificate, name='verify_with_id'),
    path('custom/<int:pk>/download/', views.download_custom_certificate, name='custom_download'),
]
