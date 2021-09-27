from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from presentaciones.models import Conferencia
from django.utils.safestring import mark_safe

# Create your views here.
def en_vivo(request):
    fecha = timezone.now()
    conferencias = Conferencia.objects.filter(
        fecha_hora__lte=fecha
    ).order_by('lugar')

    conferencias_filtradas = []
    texto_en_vivo = ""
    for conferencia in conferencias:
        if (conferencia.fecha_hora + conferencia.duracion > fecha):
            conferencias_filtradas.append(conferencia)

    if len(list(conferencias_filtradas)) == 0:
        texto_en_vivo = "Por el momento no hay conferencias en vivo. "
    else:
        texto_en_vivo = " "
        for conferencia in conferencias_filtradas:
            if conferencia.lugar == "0":
                texto_en_vivo += "Aula Magna - " + conferencia.titulo + " • "
            else:
                texto_en_vivo += "Sala " + conferencia.lugar + " - " + conferencia.titulo + " • "

    while len(texto_en_vivo) < 75:
        texto_en_vivo += texto_en_vivo

    return HttpResponse(texto_en_vivo)

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
                return render(request, 'conferencia.html', {
                    "conferencia": None,
                    "fin": None,
                })
            return redirect(f"/evento/{conferencias_filtradas[0].uuid}")
        else:
            try:
                conferencia = Conferencia.objects.get(
                    uuid=conf_uid
                )
            except:
                return redirect(f"/evento")
                
            return render(request, 'conferencia.html', {
                "conferencia": conferencia,
                "fin": conferencia.fecha_hora + conferencia.duracion,
            })

    else:
        return redirect("/entrar")
