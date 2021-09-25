from django.urls import path
from presentaciones import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.home, name='home'),
    path('informacion', views.informacion, name='info'),
    path('horarios', views.horarios, name='horarios'),

    path('conferencia/sala/<int:id_sala>', views.visitar_sala, name='sala'),
    path('conferencia/<uuid:conf_uid>', views.conferencia, name='conferencia'),
    path('conferencia/envivo', views.en_vivo, name='envivo'),
]
