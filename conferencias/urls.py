from django.urls import path
from conferencias import views

urlpatterns = [
    path('registro', views.prerregistro, name='prerregistro'),
]
