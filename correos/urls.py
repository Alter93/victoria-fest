from django.urls import path
from correos import views

urlpatterns = [
    path('marcar/<int:id>', views.marcar, name='home'),
]
