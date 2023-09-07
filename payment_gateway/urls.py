from django.urls import path
from .import views

urlpatterns = [
    path('', views.payment_form, name='payment_form'),
    path('confirmation/', views.payment_confirmation, name='payment_confirmation'),
]