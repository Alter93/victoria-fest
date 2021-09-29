from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string

from .prerregistro_form import PrerregistroForm
from .models import Prerregistro
from presentaciones.models import Conferencia
from correos.views import crear_correo

# Create your views here.
def gracias(request):
    if 'prerregistro'in request.session:
        pagina = render(request, 'home.html', {"gracias": True, "texto_boton": "REGISTRARME"})

        del request.session['prerregistro']
    else:
        pagina = redirect("/")
    return pagina


def home(request):
    fecha = timezone.now()
    conferencias_pasado = Conferencia.objects.filter(
        fecha_hora__lte=fecha
    )
    conferencias_pasado = [x for x in conferencias_pasado if not (x.fecha_hora + x.duracion >= fecha)]

    conferencias_presente = Conferencia.objects.filter(
        fecha_hora__lte=fecha
    )
    conferencias_presente = [x for x in conferencias_presente if (x.fecha_hora + x.duracion >= fecha)]
    conferencias_futuro = Conferencia.objects.filter(
        fecha_hora__gt=fecha
    )
    if 'email' in request.session:
        return render(request, 'EventoHome.html', {
            "texto_boton": "REGISTRARME",
            "conferencias_pasado": conferencias_pasado,
            "conferencias_presente": conferencias_presente,
            "conferencias_futuro": conferencias_futuro,

        })
    return render(request, 'home.html', {"texto_boton": "REGISTRARME"})


def stations(request):
    if 'email' in request.session:
        return render(request, 'stations.html', {})
    else:
        return redirect("/")


def prerregistro(request):
    if request.method == 'POST':
        form = PrerregistroForm(request.POST)
        if form.is_valid():
            ## Insertar mensaje a BD
            try:
                usuario = Prerregistro.objects.get(email=form.cleaned_data.get('email'))
                return render(request, 'prerregistro.html', {
                    "error": "Ese correo ya ha sido registrado, por favor usa uno diferente.",
                    "visibilidad":"visible",
                    "class": 'show',
                    "texto_boton": "REGISTRARME"
                 })
            except Prerregistro.DoesNotExist:
                registro = Prerregistro(
                    nombre = form.cleaned_data.get('nombre'),
                    apellido = form.cleaned_data.get('apellido'),
                    email = form.cleaned_data.get('email'),
                    genero = form.cleaned_data.get('genero'),
                    telefono = form.cleaned_data.get('telefono'),
                    lugar = form.cleaned_data.get('lugar'),
                    recibir_correos = form.cleaned_data.get('recibir_correos'),
                    emprendedor = form.cleaned_data.get('emprendedor'),
                )


                subject = 'Gracias por registrarte'
                email_from = "contacto@victoria147.org"
                recipient_list = [form.cleaned_data.get('email'),]
                registro.save()
                id_mail = crear_correo(subject, registro)
                contenido = render_to_string(
                    'email_prerregistro.html', {
                        "nombre": form.cleaned_data.get('nombre'),
                        "idmail": id_mail,
                    }
                )
                ##request.session['email'] = form.cleaned_data.get('email')
                message = contenido
                send_mail( subject, message, email_from, recipient_list , html_message=contenido)
                form = PrerregistroForm()
                request.session['prerregistro'] = 1

                return redirect('/gracias')
        else:

            return render(request, 'prerregistro.html', {"error": form.errors, "visibilidad":"visible", "class": 'show', "texto_boton": "REGISTRARME"})
    else:
        pagina = render(request, 'prerregistro.html', {"error": "", "visibilidad":"hidden", "texto_boton": "REGISTRARME"})
        if request.path == "/registro":
            pagina = render(request, 'prerregistro.html', {"error": "", "visibilidad":"visible","class":"show", "texto_boton": "REGISTRARME"})
        return pagina
