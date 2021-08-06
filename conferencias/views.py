from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .prerregistro_form import PrerregistroForm
from .models import Prerregistro



# Create your views here.

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
                    "class": 'show'
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
                registro.save()
                contenido = render_to_string(
                    'email_prerregistro.html', {
                        "nombre": form.cleaned_data.get('nombre'),
                    }
                )
                subject = 'Gracias por registrarte'
                message = contenido
                email_from = "info@altec.dev"
                recipient_list = [form.cleaned_data.get('email'),]
                send_mail( subject, message, email_from, recipient_list , html_message=contenido)
                form = PrerregistroForm()
                return render(request, 'prerregistro.html', {
                    "error": "Registro guardado con éxito.",
                    "visibilidad":"visible",
                    "class": 'show'
                    })
        else:

            return render(request, 'prerregistro.html', {"error": form.errors, "visibilidad":"visible", "class": 'show'})
    else:
        return render(request, 'prerregistro.html', {"error": "", "visibilidad":"hidden"})
