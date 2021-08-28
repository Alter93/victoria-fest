from django.urls import path
from conferencias import views

urlpatterns = [
    path('', views.prerregistro, name='prerregistro'),
    path('registro', views.prerregistro, name='prerregistro'),
    path('paginahome', views.home, name='home'),
]
