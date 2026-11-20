from django.urls import path
from . import views

app_name = 'portofolio'
urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/send/', views.send_message, name='send_message'),
]
