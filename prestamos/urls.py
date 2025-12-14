from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('bibliotecario/', views.panel_bibliotecario, name='panel_bibliotecario'),
    path('usuario/', views.panel_usuario, name='panel_usuario'),
    
    path('crear_solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('solicitud/<int:pk>/<str:accion>/', views.gestionar_solicitud, name='gestionar_solicitud'),
    
    path('devolucion/<int:prestamo_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('inicio/', views.redireccion_inteligente, name='inicio_smart'),
]