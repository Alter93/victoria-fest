from django.urls import path
from presentaciones import views

urlpatterns = [
    path('', views.conferencia, name='conferencia'),
    path('<uuid:conf_uid>', views.conferencia, name='conferencia_uuid'),
]
