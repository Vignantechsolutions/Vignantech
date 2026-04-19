from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('corporate-training/', views.corporate_training, name='corporate_training'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
]
