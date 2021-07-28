from django import forms
from django.core.exceptions import ValidationError

class PrerregistroForm(forms.Form):
    # Nombre
    # Apellido
    # Género (M- F- NO BINARIO- PREFIERO NO DECIRLO)
    # Email
    # Tel  (selección de un país) + número  / 12 dígitos  (opcional)
    # Lugar de residencia*
    # ¿Estás interesad@ en recibir correos informativos sobre los programas de Victoria147?
    # ¿Eres emprendedor/a?
    # opciones:
    # No, no soy emprendedor/a .
    # Tengo una idea de negocio.
    # Acabo de iniciar un negocio (menos de 2 años)
    # Tengo un negocio en crecimiento (2 a 5 años)
    # Tengo un negocio en expansión (más de 5 años).

    nombre = forms.CharField(max_length=100, error_messages={
        'required': 'Ingresa tu nombre completo.'
    })
    apellido = forms.CharField(max_length=100, error_messages={
        'required': 'Ingresa tu apellido.'
    })
    email = forms.EmailField(error_messages={
        'required': 'Ingresa tu email.'
    })

    genero_choices =(
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("No Binario", "No binario"),
        ("NA", "Prefiero no decir.")
    )
    genero = forms.ChoiceField(choices = genero_choices)

    codigo_pais = forms.CharField(max_length=4,error_messages={
        'invalid': 'Selecciona un código de pais.'
    })
    telefono = forms.CharField(max_length=11, error_messages={
        'required': 'Ingresa un número telefónico (10 digitos)'
    })

    lugar = forms.CharField(max_length=100, error_messages={
        'required': 'Selecciona un lugar de residencia.'
    })
    recibir_correos = forms.BooleanField(required = False)


    emprendedor_choices =(
        ("No", "No, no soy emprendedor/a."),
        ("Tengo una idea de negocio.", "Tengo una idea de negocio."),
        ("Acabo de iniciar un negocio (menos de 2 años).", "Acabo de iniciar un negocio (menos de 2 años)."),
        ("Tengo un negocio en crecimiento (2 a 5 años).", "Tengo un negocio en crecimiento (2 a 5 años)."),
        ("Tengo un negocio en expansión (más de 5 años).", "Tengo un negocio en expansión (más de 5 años)."),
    )
    emprendedor = forms.ChoiceField(choices = emprendedor_choices)
