import json

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from presentaciones.models import Conferencia, EntrarForm
from conferencias.models import Prerregistro
from django.utils.safestring import mark_safe

# Create your views here.
def verificar(request, username=None):
    try:
        user = Prerregistro.objects.get(email=username)
        request.session['email'] = username
    except Prerregistro.DoesNotExist:
        return None

    return user

def entrar(request):
    if 'email' in request.session:
        return redirect("/")

    if request.method == 'POST':
        form = EntrarForm(request.POST)
        if form.is_valid():
            user = verificar(request, username=form.cleaned_data.get('email'))
            if user == None:
                return render(request, 'LoginEvento.html', {
                    "error_login": "El email no esta registrado. Favor de registrarse para poder acceder al evento.",
                    "texto_boton": "REGISTRARME"
                })
            else:
                return redirect("/")
    else:
        return render(request, 'LoginEvento.html', {"texto_boton": "REGISTRARME"})


def salir(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect("/")

def envivo(request):
    fecha = timezone.now()
    conferencias = Conferencia.objects.filter(
        fecha_hora__lte=fecha
    )

    conferencias_filtradas = []
    texto_en_vivo = ""
    for conferencia in conferencias:
        if (conferencia.fecha_hora + conferencia.duracion > fecha):
            conferencias_filtradas.append(conferencia)

    if len(list(conferencias_filtradas)) == 0:
        texto_en_vivo = "Por el momento no hay conferencias en vivo. ✱ "
    else:
        texto_en_vivo = " EN VIVO ● " + conferencias_filtradas[0].titulo + " ✱ "

    while len(texto_en_vivo) < 75:
        texto_en_vivo = texto_en_vivo + texto_en_vivo

    return HttpResponse(mark_safe(texto_en_vivo))

def conferencia(request, conf_uid = None):
    fecha = timezone.now()
    if 'email' in request.session:
        if conf_uid == None:
            conferencias_filtradas = []
            conferencias = Conferencia.objects.filter(
                fecha_hora__lte=fecha
            )
            for conferencia in conferencias:
                if (conferencia.fecha_hora + conferencia.duracion > fecha):
                    conferencias_filtradas.append(conferencia)
            if len(conferencias_filtradas) < 1:
                return redirect("/#agenda")

            return redirect(f"/evento/{conferencias_filtradas[0].uuid}")
        else:
            try:
                conferencia = Conferencia.objects.get(
                    uuid=conf_uid
                )
                if (not conferencia.fecha_hora + conferencia.duracion > fecha
                or not conferencia.fecha_hora < fecha):
                    return redirect(f"/evento")
            except:
                return redirect(f"/evento")

            return render(request, 'conferencia.html', {
                "conferencia": conferencia
            })

    else:
        return redirect("entrar")

def cargar_url(request):
    fecha = timezone.now()
    response_json = {}

    conferencias_filtradas = []
    conferencias = Conferencia.objects.filter(
        fecha_hora__lte=fecha
    )
    for conferencia in conferencias:
        if (conferencia.fecha_hora + conferencia.duracion > fecha):
            conferencias_filtradas.append(conferencia)
    if len(conferencias_filtradas) < 1:
        url = "/evento/"
        response_json['url'] = url
        response_json['titulo'] = "No hay ningun evento"
        response_json['horario'] = ""
        response_json['speaker'] = ""
        response_json['color'] = "gradientMorado"
    else:
        url = f"/evento/{conferencias_filtradas[0].uuid}"
        response_json['url'] = url
        response_json['reprograma'] = conferencias_filtradas[0].reprograma
        response_json['color'] = conferencias_filtradas[0].color
        response_json['titulo'] = conferencias_filtradas[0].titulo
        response_json['horario'] = timezone.localtime(conferencias_filtradas[0].fecha_hora).strftime("%H:%M") + " - " + timezone.localtime(conferencias_filtradas[0].fecha_fin).strftime("%H:%M")
        response_json['speaker'] = conferencias_filtradas[0].id_conferencista.nombre + " " + conferencias_filtradas[0].id_conferencista.apellido

    return HttpResponse(json.dumps(response_json),content_type="application/json")
