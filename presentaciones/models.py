import uuid
from django.db import models

# Create your models here.
class Conferencista(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    biografia = models.CharField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)

class Conferencia(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000,null=True, blank=True)
    fecha_hora = models.DateTimeField()
    duracion = models.DurationField()
    vimeo = models.CharField(max_length=200,null=True, blank = True)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    color = models.CharField(max_length=200,null=True, blank = True)

    def __str__(self):
        return '%s %s' % (self.titulo, self.fecha_hora)
