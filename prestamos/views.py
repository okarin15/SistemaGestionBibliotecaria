from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .models import Socio, SolicitudPrestamo


# ---------- LOGIN / LOGOUT ----------

class CustomLoginView(LoginView):
    template_name = "prestamos/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            # Bibliotecario
            return reverse_lazy("panel_bibliotecario")
        if hasattr(user, "socio"):
            # Usuario asociado a Socio
            return reverse_lazy("panel_usuario")
        # Por defecto, lo mandamos al panel de bibliotecario
        return reverse_lazy("panel_bibliotecario")


class CustomLogoutView(LogoutView):
    # Siempre redirigir al login después de cerrar sesión
    next_page = reverse_lazy("login")

    def get_next_page(self):
        """
        Forzamos que, independiente de ?next= en la URL,
        siempre vuelva al login.
        """
        return self.next_page


# ---------- PANEL BIBLIOTECARIO ----------

@login_required
@user_passes_test(lambda u: u.is_staff)
def panel_bibliotecario(request):
    """
    Panel del bibliotecario:
    - Ve las solicitudes de préstamo realizadas desde el portal de usuarios.
    """
    solicitudes = SolicitudPrestamo.objects.select_related("socio__user").order_by(
        "-fecha_solicitud"
    )

    return render(request, "prestamos/sgb.html", {
        "usuario": request.user,
        "rol": "Bibliotecario",
        "solicitudes": solicitudes,
    })


# ---------- PANEL USUARIO ----------

@login_required
def panel_usuario(request):
    """
    Panel del socio:
    - Ve sus propias solicitudes de préstamo.
    """
    nombre_socio = request.user.get_full_name() or request.user.username

    solicitudes = []
    if hasattr(request.user, "socio"):
        solicitudes = SolicitudPrestamo.objects.filter(
            socio=request.user.socio
        ).order_by("-fecha_solicitud")

    return render(request, "prestamos/panel_usuario.html", {
        "usuario": request.user,
        "rol": "Socio",
        "nombre_socio": nombre_socio,
        "solicitudes": solicitudes,
    })


# ---------- CREAR SOLICITUD DE PRÉSTAMO (USUARIO) ----------

@login_required
def crear_solicitud(request):
    """
    Vista que recibe el formulario del usuario (socio) para solicitar un libro.
    """
    if request.method != "POST":
        return redirect("panel_usuario")

    if not hasattr(request.user, "socio"):
        messages.error(request, "Tu usuario no está asociado a un socio.")
        return redirect("panel_usuario")

    titulo = request.POST.get("titulo_libro", "").strip()
    if not titulo:
        messages.error(request, "Debes elegir un libro para solicitar.")
        return redirect("panel_usuario")

    SolicitudPrestamo.objects.create(
        socio=request.user.socio,
        titulo_libro=titulo,
        estado="pendiente",
    )

    messages.success(request, "¡Solicitud enviada al bibliotecario!")
    return redirect("panel_usuario")


# ---------- GESTIONAR SOLICITUD (BIBLIOTECARIO) ----------

@login_required
@user_passes_test(lambda u: u.is_staff)
def gestionar_solicitud(request, pk, accion):
    """
    Permite al bibliotecario aprobar o rechazar una solicitud de préstamo.
    pk     -> id de la solicitud
    accion -> 'aprobar' o 'rechazar'
    """
    solicitud = get_object_or_404(SolicitudPrestamo, pk=pk)

    if accion == "aprobar":
        solicitud.estado = "aprobado"
        messages.success(
            request,
            f"Solicitud de '{solicitud.titulo_libro}' APROBADA."
        )
    elif accion == "rechazar":
        solicitud.estado = "rechazado"
        messages.warning(
            request,
            f"Solicitud de '{solicitud.titulo_libro}' RECHAZADA."
        )
    else:
        messages.error(request, "Acción no válida.")

    solicitud.save()
    return redirect("panel_bibliotecario")