from django.db import models
from conferencias.models import Prerregistro

# Create your models here.
class Correo(models.Model):
    asunto = models.CharField(max_length=250)
    usuario = models.ForeignKey(Prerregistro, on_delete=models.CASCADE, null=True)
    leido = models.IntegerField()
