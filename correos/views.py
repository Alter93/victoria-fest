from django.http import HttpResponse
from django.shortcuts import render
from correos.models import Correo

# Create your views here.


def marcar(request, id):
    with open("correos/pixel.png", 'rb') as fh:
        pixel = fh.read()

    correo = Correo.objects.get(id=id)
    correo.leido = 1
    correo.save()
    return HttpResponse(pixel, content_type='image/png')


def crear_correo(asunto, prerregistro):
    correo = Correo(
        asunto = asunto,
        usuario = prerregistro,
        leido = 0
    )
    correo.save()

    return correo.id
