from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView
from .views import (
    # API
    ClienteViewSet, VeterinarioViewSet, MascotaViewSet, CitaViewSet, 
    AtencionViewSet, ListaEsperaViewSet, ProductoViewSet,
    # Frontend
    index, servicios, dashboard_recepcion, dashboard_veterinario, 
    dashboard_cliente, CustomLoginView, registro, registro_rapido,
    crear_cita_recepcion, cancelar_cita, historial_mascota, quienes_somos, contacto,
    # New
    api_citas_calendario, reagendar_cita, editar_cliente, editar_mascota, registrar_atencion,
    # HU002 y HU006
    api_disponibilidad_horarios, api_antecedentes_mascota, cancelar_cita_veterinario,
    # Cliente
    agregar_mascota_cliente,
    # API Views
    guardar_atencion, registrar_atencion_walkin
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'veterinarios', VeterinarioViewSet)
router.register(r'mascotas', MascotaViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'atenciones', AtencionViewSet)
router.register(r'lista-espera', ListaEsperaViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    # API
    # API - Custom endpoints must be before router to avoid being caught as PKs
    path('citas/calendario/', api_citas_calendario, name='api_citas_calendario'),
    # HU002: Disponibilidad de horarios
    path('disponibilidad/', api_disponibilidad_horarios, name='api_disponibilidad_horarios'),
    # HU006: Antecedentes de mascota
    path('mascotas/<int:mascota_id>/antecedentes/', api_antecedentes_mascota, name='api_antecedentes_mascota'),
    path('', include(router.urls)),
    
    # Frontend Pages
    path('inicio/', index, name='index'),
    path('servicios/', servicios, name='servicios'),
    
    # Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    
    # Dashboards
    path('dashboard/recepcion/', dashboard_recepcion, name='dashboard_recepcion'),
    path('dashboard/veterinario/', dashboard_veterinario, name='dashboard_veterinario'),
    path('dashboard/cliente/', dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/cliente/agregar_mascota/', agregar_mascota_cliente, name='agregar_mascota_cliente'),
    path('dashboard/registro_rapido/', registro_rapido, name='registro_rapido'),
    path('dashboard/crear_cita/', crear_cita_recepcion, name='crear_cita_recepcion'),
    path('dashboard/cancelar_cita/<int:cita_id>/', cancelar_cita, name='cancelar_cita'),
    path('dashboard/reagendar_cita/<int:cita_id>/', reagendar_cita, name='reagendar_cita'),
    path('dashboard/editar_cliente/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('dashboard/editar_mascota/<int:mascota_id>/', editar_mascota, name='editar_mascota'),
    path('dashboard/veterinario/historial/<int:mascota_id>/', historial_mascota, name='historial_mascota'),
    path('dashboard/veterinario/atender/<int:cita_id>/', registrar_atencion, name='registrar_atencion'),
    # HU006: Cancelar cita por veterinario
    path('dashboard/veterinario/cancelar_cita/<int:cita_id>/', cancelar_cita_veterinario, name='cancelar_cita_veterinario'),
    # Guardar Atención
    path('api/citas/<int:cita_id>/guardar_atencion/', guardar_atencion, name='guardar_atencion'),
    # Walk-in Atención
    path('api/lista-espera/<int:lista_id>/registrar_atencion/', registrar_atencion_walkin, name='registrar_atencion_walkin'),
    path('quienes-somos/', quienes_somos, name='quienes_somos'),
    path('contacto/', contacto, name='contacto'),
]
