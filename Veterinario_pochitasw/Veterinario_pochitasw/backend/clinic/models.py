from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Validadores (permisivos para testing)
phone_validator = RegexValidator(
    regex=r'^(\+?56)?9?\d{7,9}$',
    message="El teléfono debe ser un número válido."
)

rut_validator = RegexValidator(
    regex=r'^\d{1,2}\.?\d{1,3}\.?\d{1,3}-?[\dkK]$',
    message="El RUT debe tener un formato válido."
)

class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrador')
        VETERINARIO = 'VETERINARIO', _('Veterinario')
        RECEPCIONISTA = 'RECEPCIONISTA', _('Recepcionista')
        CLIENTE = 'CLIENTE', _('Cliente')

    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CLIENTE
    )

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_cliente', null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, validators=[rut_validator])
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, validators=[phone_validator])
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"

class Veterinario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_veterinario', null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, validators=[rut_validator])
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, default='General')
    telefono = models.CharField(max_length=15, validators=[phone_validator])

    def __str__(self):
        return f"Dr. {self.nombre} ({self.especialidad})"

class Mascota(models.Model):
    class Especie(models.TextChoices):
        PERRO = 'Perro', _('Perro')
        GATO = 'Gato', _('Gato')
    
    class Genero(models.TextChoices):
        MACHO = 'Macho', _('Macho')
        HEMBRA = 'Hembra', _('Hembra')

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=Especie.choices, default=Especie.PERRO)
    genero = models.CharField(max_length=10, choices=Genero.choices, default=Genero.MACHO)
    raza = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_registro = models.DateField(default=timezone.now)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - Dueño: {self.cliente.nombre}"

    @property
    def edad_aprox(self):
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None

class Cita(models.Model):
    class Estado(models.TextChoices):
        AGENDADA = 'AGENDADA', _('Agendada')
        CONFIRMADA = 'CONFIRMADA', _('Confirmada')
        REALIZADA = 'REALIZADA', _('Realizada')
        CANCELADA = 'CANCELADA', _('Cancelada')
        NO_ASISTE = 'NO_ASISTE', _('No Asiste')
    
    class Tipo(models.TextChoices):
        CONSULTA = 'CONSULTA', _('Consulta General')
        CONTROL = 'CONTROL', _('Control / Revisión')
        VACUNA = 'VACUNA', _('Vacunación')
        CIRUGIA = 'CIRUGIA', _('Cirugía')
        URGENCIA = 'URGENCIA', _('Urgencia')

    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, related_name='citas')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.CONSULTA)
    motivo = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.AGENDADA)
    es_urgencia = models.BooleanField(default=False, verbose_name=_("Es Urgencia"))
    
    # Campo helper para saber si ya se procesó en atención
    
    def __str__(self):
        return f"Cita: {self.mascota.nombre} con Dr. {self.veterinario.nombre if self.veterinario else 'Sin asignar'} - {self.fecha_hora}"

class ListaEspera(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', _('Pendiente')
        CONTACTADO = 'CONTACTADO', _('Contactado')
        CERRADO = 'CERRADO', _('Cerrado') # Ya agendó o desistió

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='lista_espera')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    preferencia = models.TextField(help_text="Preferencia de horario o doctor")

    def __str__(self):
        return f"Espera: {self.cliente.nombre} - {self.fecha_solicitud}"

class Atencion(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='atencion')
    fecha = models.DateTimeField(default=timezone.now)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    medicamentos = models.TextField(blank=True)
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=0, default=0) # CLP sin decimales
    requiere_operacion = models.BooleanField(default=False)
    
    # Si requiere operación, se planifican revisiones (logica en vista)

    def __str__(self):
        return f"Atención {self.id} - {self.cita.mascota.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        super().save(*args, **kwargs)
