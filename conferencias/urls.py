from django.urls import path
from conferencias import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entrar', views.entrar, name='entrar'),
    path('salir', views.salir, name='salir'),
    path('registro', views.prerregistro, name='prerregistro'),
    path('gracias', views.gracias, name='gracias'),
    path('stations', views.stations, name='stations')
]
