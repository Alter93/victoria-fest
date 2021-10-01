import uuid
from django.db import models
from django.utils.text import slugify
from django import forms

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
    uuid = models.SlugField(primary_key=False, editable=False)
    color = models.CharField(max_length=200,null=True, blank = True)
    id_conferencista = models.ForeignKey('Conferencista', on_delete=models.CASCADE, null=True, blank=True)
    reprograma = models.IntegerField(null=True, blank = True)

    @property
    def fecha_fin(self):
        return self.fecha_hora + self.duracion

    def save(self, *args, **kwargs):
        self.uuid = slugify(self.titulo)
        super(Conferencia, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.titulo, self.fecha_hora)

class EntrarForm(forms.Form):
    email = forms.EmailField(error_messages={
        'required': 'Ingresa tu email.'
    })
