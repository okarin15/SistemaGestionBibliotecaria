from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from .models import Libro, SolicitudPrestamo, Prestamo
from .forms import SolicitudForm

# --- CONFIGURACIÓN ---
VALOR_MULTA_DIARIA = 1000  # $1.000 por día de atraso (Ajustable)

# --- AUTENTICACIÓN ---

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('panel_bibliotecario')
        return reverse_lazy('panel_usuario')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# --- PANELES ---

@login_required
@user_passes_test(lambda u: u.is_staff)
def panel_bibliotecario(request):
    # 1. Solicitudes Pendientes
    solicitudes = SolicitudPrestamo.objects.filter(estado='pendiente')
    
    # 2. Préstamos Activos (Calculando deuda en vivo)
    prestamos_activos = Prestamo.objects.filter(fecha_devolucion_real__isnull=True)
    ahora = timezone.now()
    
    for prestamo in prestamos_activos:
        if prestamo.fecha_devolucion_esperada < ahora:
            diferencia = ahora - prestamo.fecha_devolucion_esperada
            dias = diferencia.days + 1
            prestamo.multa_temporal = dias * VALOR_MULTA_DIARIA
            prestamo.dias_temporal = dias
        else:
            prestamo.multa_temporal = 0
            prestamo.dias_temporal = 0

    # 3. Historial de Infracciones (Multas ya cerradas)
    # Filtramos préstamos que ya tienen fecha de devolución y cuyo monto de multa fue mayor a 0
    historial_multas = Prestamo.objects.filter(
        fecha_devolucion_real__isnull=False,
        monto_multa__gt=0
    ).order_by('-fecha_devolucion_real')

    return render(request, 'sgb.html', {
        'solicitudes': solicitudes,
        'prestamos': prestamos_activos,
        'historial_multas': historial_multas,  
        'hoy': ahora
    })

@login_required
def panel_usuario(request):
    socio = request.user.socio
    ahora = timezone.now()

    # 1. Datos básicos (Tablas)
    mis_solicitudes = SolicitudPrestamo.objects.filter(socio=socio).order_by('-fecha_solicitud')
    prestamos_activos = Prestamo.objects.filter(solicitud__socio=socio, fecha_devolucion_real__isnull=True)
    libros_disponibles = Libro.objects.filter(estado='disponible')

    # 2. ESTADÍSTICAS (La magia nueva)
    # A. Total de libros pedidos históricamente
    total_pedidos = SolicitudPrestamo.objects.filter(socio=socio, estado='finalizado').count()
    
    # B. Libros que tiene en su poder ahora mismo
    en_poder = prestamos_activos.count()

    # C. Total de dinero pagado en multas (Suma histórica)
    # Usamos 'aggregate' de Django para sumar la columna 'monto_multa'
    total_multas = Prestamo.objects.filter(solicitud__socio=socio).aggregate(Sum('monto_multa'))['monto_multa__sum'] or 0

    return render(request, 'panel_usuario.html', {
        'solicitudes': mis_solicitudes,
        'prestamos': prestamos_activos,
        'libros': libros_disponibles,
        'hoy': ahora,
        # Pasamos los datos nuevos
        'stats': {
            'total_pedidos': total_pedidos,
            'en_poder': en_poder,
            'total_multas': total_multas
        }
    })

# --- GESTIÓN DE PRÉSTAMOS (CORE) ---

@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.socio = request.user.socio
            solicitud.save()
            
            # Marcar libro como prestado
            libro = solicitud.libro
            libro.estado = 'prestado'
            libro.save()
            
            messages.success(request, "¡Solicitud enviada correctamente!")
            return redirect('panel_usuario')
    else:
        # Solo mostramos libros disponibles
        form = SolicitudForm()
        form.fields['libro'].queryset = form.fields['libro'].queryset.filter(estado='disponible')

    # AQUÍ está la clave: Vamos a crear este archivo ahora
    return render(request, 'crear_solicitud.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def gestionar_solicitud(request, pk, accion):
    solicitud = get_object_or_404(SolicitudPrestamo, pk=pk)

    if accion == 'aprobar':
        # 1. Cambiar estado
        solicitud.estado = 'aprobado'
        solicitud.save()
        
        # 2. Crear el Préstamo oficial (Esto activa el reloj de 7 días)
        Prestamo.objects.create(solicitud=solicitud)
        
        # 3. Marcar libro como no disponible
        solicitud.libro.estado = 'prestado'
        solicitud.libro.save()

        messages.success(request, "Préstamo aprobado e iniciado correctamente.")

    elif accion == 'rechazar':
        solicitud.estado = 'rechazado'
        solicitud.save()
        messages.info(request, "Solicitud rechazada.")

    return redirect('panel_bibliotecario')

@login_required
@user_passes_test(lambda u: u.is_staff)
def registrar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # 1. Marcar fecha real de devolución 
    prestamo.fecha_devolucion_real = timezone.now()
    
    # 2. CÁLCULO DE MULTA 
    # Si la fecha real es mayor a la esperada, calculamos la diferencia
    if prestamo.fecha_devolucion_real > prestamo.fecha_devolucion_esperada:
        diferencia = prestamo.fecha_devolucion_real - prestamo.fecha_devolucion_esperada
        # Convertimos la diferencia a días (redondeando hacia arriba si pasó aunque sea 1 minuto)
        dias_retraso = diferencia.days
        if dias_retraso > 0:
            prestamo.dias_atraso = dias_retraso
            prestamo.monto_multa = dias_retraso * VALOR_MULTA_DIARIA
            messages.warning(request, f"Devolución con retraso. Multa generada: ${prestamo.monto_multa}")
        else:
            messages.success(request, "Libro devuelto a tiempo. Sin multa.")
    else:
        messages.success(request, "Libro devuelto a tiempo.")

    # 3. Finalizar la solicitud y liberar el libro
    prestamo.solicitud.estado = 'finalizado'
    prestamo.solicitud.save()
    
    libro = prestamo.solicitud.libro
    libro.estado = 'disponible'
    libro.save()
    
    prestamo.save()
    return redirect('panel_bibliotecario')

def redireccion_inteligente(request):
    """
    Si no está logueado -> Login
    Si es Admin -> Panel Bibliotecario
    Si es Usuario -> Panel Usuario
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_staff:
        return redirect('panel_bibliotecario')
    else:
        return redirect('panel_usuario')