from django.urls import path
from presentaciones import views

urlpatterns = [
    path('<int:conf_uid>', views.conferencia, name='conferencia'),
]
