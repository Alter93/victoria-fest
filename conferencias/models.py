from django.db import models

# Create your models here.
class Prerregistro(models.Model):
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

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    genero = models.CharField(max_length=20)
    telefono = models.CharField(max_length=16, null=True, blank=True)
    lugar = models.CharField(max_length=100, null=True, blank=True)
    recibir_correos = models.BooleanField()
    emprendedor = models.CharField(max_length=100)

    class Meta:
        db_table = "prerregistro"
