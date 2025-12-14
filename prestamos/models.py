from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# --- Modelos Base ---

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default="disponible") # disponible, prestado

    def __str__(self):
        return self.titulo

# --- Gestión de Usuarios ---

class Socio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="socio")
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# --- Flujo de Préstamos ---

class SolicitudPrestamo(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
        ("finalizado", "Finalizado"),
    ]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="solicitudes")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    def __str__(self):
        titulo = self.libro.titulo if self.libro else "Sin libro"
        return f"{titulo} - {self.socio} ({self.estado})"

class Prestamo(models.Model):
    solicitud = models.OneToOneField(SolicitudPrestamo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    
    # Auditoría y Multas (Req. Eva 4)
    monto_multa = models.IntegerField(default=0)
    dias_atraso = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Al crear, setear devolución a 7 días
        if not self.id:
            self.fecha_devolucion_esperada = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Préstamo #{self.id} - {self.solicitud.socio}"