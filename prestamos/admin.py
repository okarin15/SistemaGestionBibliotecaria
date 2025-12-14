from django.contrib import admin
from .models import Socio, Autor, Libro, SolicitudPrestamo, Prestamo

# Registro de Autores
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'nacionalidad')

# Registro de Libros
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'estado')
    list_filter = ('estado', 'categoria')
    search_fields = ('titulo', 'autor__nombre')

# Registro de Socios
@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'telefono', 'direccion')
    search_fields = ('rut', 'user__username')

# Registro de Solicitudes 
@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'socio', 'fecha_solicitud', 'estado')
    list_filter = ('estado',)

# Registro de Préstamos Activos 
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitud', 'fecha_devolucion_esperada', 'monto_multa', 'dias_atraso')
    list_filter = ('fecha_prestamo',)