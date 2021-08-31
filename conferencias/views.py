from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .prerregistro_form import PrerregistroForm
from .models import Prerregistro
from correos.views import crear_correo



# Create your views here.
def home(request):
    return render(request, 'home.html', {})

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
                    "texto_boton": "UNIRME"
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
                email_from = "paola@victoria147.org"
                recipient_list = [form.cleaned_data.get('email'),]
                registro.save()
                id_mail = crear_correo(subject, registro)
                contenido = render_to_string(
                    'email_prerregistro.html', {
                        "nombre": form.cleaned_data.get('nombre'),
                        "idmail": id_mail,
                    }
                )

                message = contenido
                send_mail( subject, message, email_from, recipient_list , html_message=contenido)
                form = PrerregistroForm()

                return render(request, 'prerregistro.html', {
                    "error": "Registro guardado con éxito. ¡Ya eres parte del VictoriaFest! Revisa tu email para más información.",
                    "visibilidad":"visible",
                    "class": 'show',
                    "texto_boton": "Listo!"
                    })
        else:

            return render(request, 'prerregistro.html', {"error": form.errors, "visibilidad":"visible", "class": 'show', "texto_boton": "UNIRME"})
    else:
        return render(request, 'prerregistro.html', {"error": "", "visibilidad":"hidden", "texto_boton": "UNIRME"})
