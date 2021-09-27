from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .prerregistro_form import PrerregistroForm, EntrarForm
from .models import Prerregistro
from correos.views import crear_correo

def verificar(request, username=None):
    try:
        user = Prerregistro.objects.get(email=username)
        request.session['email'] = username
    except Prerregistro.DoesNotExist:
        return None

    return user


# Create your views here.
def gracias(request):
    if 'prerregistro'in request.session:
        pagina = render(request, 'home.html', {"gracias": True, "texto_boton": "REGISTRARME"})
        request.session['email'] = username
        del request.session['prerregistro']
    else:
        pagina = redirect("/")
    return pagina

def entrar(request):
    if 'email' in request.session:
        return redirect("/")

    if request.method == 'POST':
        form = EntrarForm(request.POST)
        if form.is_valid():
            user = verificar(request, username=form.cleaned_data.get('email'))
            if user == None:
                return render(request, 'LoginEvento.html', {
                    "error_login": "El email no existe. Favor de registrarse.",
                    "texto_boton": "REGISTRARME"
                })
            else:
                return redirect("/")
    else:
        return render(request, 'LoginEvento.html', {"texto_boton": "REGISTRARME"})


def salir(request):
    del request.session['email']
    return redirect("/")


def home(request):
    return render(request, 'home.html', {"texto_boton": "REGISTRARME"})

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

                message = contenido
                send_mail( subject, message, email_from, recipient_list , html_message=contenido)
                form = PrerregistroForm()
                # return render(request, 'prerregistro.html', {
                #     "error": "Registro guardado con éxito. ¡Ya eres parte del VictoriaFest! Revisa tu email para más información.",
                #     "visibilidad":"visible",
                #     "class": 'show',
                #     "texto_boton": "Listo!"
                #     })
                request.session['prerregistro'] = 1
                return redirect('/gracias')

        else:

            return render(request, 'prerregistro.html', {"error": form.errors, "visibilidad":"visible", "class": 'show', "texto_boton": "REGISTRARME"})
    else:
        pagina = render(request, 'prerregistro.html', {"error": "", "visibilidad":"hidden", "texto_boton": "REGISTRARME"})
        if request.path == "/registro":
            pagina = render(request, 'prerregistro.html', {"error": "", "visibilidad":"visible","class":"show", "texto_boton": "REGISTRARME"})
        return pagina
