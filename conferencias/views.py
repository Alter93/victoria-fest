from django.shortcuts import render
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
                    "form": form.as_ul(),
                    "error": "Ese correo ya ha sido registrado, por favor usa uno diferente."
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
                form = PrerregistroForm()
                return render(request, 'prerregistro.html', {
                    "error": "Registro guardado con éxito."
                 })
        else:
            return render(request, 'prerregistro.html', {"error": ""})
    else:
        form = PrerregistroForm()
        return render(request, 'prerregistro.html', {"error": ""})
