from django.contrib import admin
from .models import Socio, SolicitudPrestamo


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("user", "rut", "telefono")
    search_fields = ("user__username", "user__first_name", "user__last_name", "rut")


@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):
    list_display = ("titulo_libro", "socio", "estado", "fecha_solicitud")
    list_filter = ("estado", "fecha_solicitud")
    search_fields = ("titulo_libro", "socio__user__username")
