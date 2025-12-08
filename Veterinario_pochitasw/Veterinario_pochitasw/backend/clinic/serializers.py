from rest_framework import serializers
from .models import Usuario, Cliente, Veterinario, Mascota, Cita, Atencion, ListaEspera, Producto, Venta, DetalleVenta

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol']

class ClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'

class VeterinarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Veterinario
        fields = '__all__'

class MascotaSerializer(serializers.ModelSerializer):
    edad_aprox = serializers.ReadOnlyField()

    class Meta:
        model = Mascota
        fields = '__all__'

class CitaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre')
    cliente_nombre = serializers.ReadOnlyField(source='mascota.cliente.nombre')
    veterinario_nombre = serializers.ReadOnlyField(source='veterinario.nombre', allow_null=True)

    class Meta:
        model = Cita
        fields = '__all__'

class AtencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atencion
        fields = '__all__'

class ListaEsperaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre')
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre')
    veterinario_nombre = serializers.ReadOnlyField(source='veterinario_asignado.nombre')
    tiempo_espera = serializers.SerializerMethodField()
    
    class Meta:
        model = ListaEspera
        fields = '__all__'
    
    def get_tiempo_espera(self, obj):
        """Calcula el tiempo de espera en minutos"""
        if obj.estado == ListaEspera.Estado.ESPERANDO:
            from django.utils import timezone
            delta = timezone.now() - obj.fecha_solicitud
            return int(delta.total_seconds() / 60)
        return None

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
