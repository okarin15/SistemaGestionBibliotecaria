# prestamos/urls.py

from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    panel_bibliotecario,
    panel_usuario,
    crear_solicitud,
    gestionar_solicitud,  # 👈 IMPORTANTE
)

urlpatterns = [
    # Login por defecto en "/"
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # Paneles
    path("bibliotecario/", panel_bibliotecario, name="panel_bibliotecario"),
    path("usuario/", panel_usuario, name="panel_usuario"),

    # Solicitud que crea el usuario (Diego)
    path("crear_solicitud/", crear_solicitud, name="crear_solicitud"),

    # 👇 NUEVA RUTA: aprobar / rechazar desde el bibliotecario
    path(
        "solicitud/<int:pk>/<str:accion>/",
        gestionar_solicitud,
        name="gestionar_solicitud",
    ),
]
