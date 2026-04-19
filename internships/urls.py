from django.urls import path
from . import views

app_name = 'internships'

urlpatterns = [
    path('', views.internship_list, name='list'),
    path('<slug:slug>/', views.internship_detail, name='detail'),
]
