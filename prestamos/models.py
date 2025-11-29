from django.db import models
from django.contrib.auth.models import User


class Socio(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="socio"
    )
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class SolicitudPrestamo(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ]

    socio = models.ForeignKey(
        Socio,
        on_delete=models.CASCADE,
        related_name="solicitudes"
    )
    titulo_libro = models.CharField(max_length=200)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    def __str__(self):
        return f"{self.titulo_libro} - {self.socio} ({self.get_estado_display()})"
