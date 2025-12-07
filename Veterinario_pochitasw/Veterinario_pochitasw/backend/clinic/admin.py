from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Veterinario, Mascota, Cita, Atencion, ListaEspera, Producto, Venta, DetalleVenta

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )

class MascotaInline(admin.TabularInline):
    model = Mascota
    extra = 0

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'telefono', 'email')
    search_fields = ('rut', 'nombre', 'apellido')
    inlines = [MascotaInline]

class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'especialidad', 'telefono')

class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'mascota', 'veterinario', 'tipo', 'estado')
    list_filter = ('estado', 'tipo', 'fecha_hora', 'veterinario')
    search_fields = ('mascota__nombre', 'mascota__cliente__rut')

class AtencionAdmin(admin.ModelAdmin):
    list_display = ('cita', 'fecha', 'diagnostico', 'requiere_operacion')

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total')
    inlines = [DetalleVentaInline]

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Veterinario, VeterinarioAdmin)
admin.site.register(Mascota)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Atencion, AtencionAdmin)
admin.site.register(ListaEspera)
admin.site.register(Producto)
admin.site.register(Venta, VentaAdmin)
