from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<str:item_type>/<int:item_id>/', views.initiate_payment, name='initiate'),
    path('callback/', views.payment_callback, name='callback'),
    path('history/', views.payment_history, name='history'),
]
