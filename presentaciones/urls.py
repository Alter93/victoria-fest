from django.urls import path
from presentaciones import views

urlpatterns = [
    path('', views.conferencia, name='conferencia'),
    path('entrar', views.entrar, name='entrar'),
    path('salir', views.salir, name='salir'),
    path('<slug:conf_uid>', views.conferencia, name='conferencia_uuid'),
]