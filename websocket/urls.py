from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('send_message/', views.send_message(, name= 'send message'))
]