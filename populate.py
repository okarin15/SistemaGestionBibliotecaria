import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')
django.setup()

from django.contrib.auth.models import User
from prestamos.models import Autor, Libro, Socio, SolicitudPrestamo, Prestamo

def poblar_datos():
    print("🔄 Iniciando script de población de datos...")

    # --- 1. CREAR SUPERUSUARIO (Bibliotecario) ---
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@biblioteca.cl', 'biblioteca1234')
        print("✅ Superusuario 'admin' creado (Clave: biblioteca1234)")
    else:
        print("ℹ️ El usuario 'admin' ya existe.")

    # --- 2. CREAR USUARIO SOCIO (Okarin) ---
    user_okarin, created = User.objects.get_or_create(
        username='okarin',
        defaults={'first_name': 'Rintaro', 'last_name': 'Okabe'}
    )
    if created:
        user_okarin.set_password('biblioteca1234')
        user_okarin.save()
        print("✅ Usuario 'okarin' creado (Clave: biblioteca1234)")
    
    # Crear su perfil de Socio
    socio_okarin, created = Socio.objects.get_or_create(
        user=user_okarin,
        defaults={
            'rut': '11.111.111-1',
            'telefono': '99999999',
            'direccion': 'Laboratorio Future Gadget'
        }
    )
    if created:
        print("✅ Perfil de Socio para Okarin creado.")

    # --- 3. CREAR AUTORES ---
    autores_data = [
        {'nombre': 'Gabriel', 'apellido': 'García Márquez', 'nacionalidad': 'Colombiana'},
        {'nombre': 'Isabel', 'apellido': 'Allende', 'nacionalidad': 'Chilena'},
        {'nombre': 'J.K.', 'apellido': 'Rowling', 'nacionalidad': 'Británica'},
    ]
    
    autores_objs = []
    for data in autores_data:
        autor, _ = Autor.objects.get_or_create(
            nombre=data['nombre'], 
            apellido=data['apellido'],
            defaults={'nacionalidad': data['nacionalidad']}
        )
        autores_objs.append(autor)
    print(f"✅ {len(autores_objs)} Autores verificados/creados.")

    # --- 4. CREAR LIBROS ---
    libros_data = [
        {'titulo': 'Cien Años de Soledad', 'cat': 'Realismo Mágico', 'autor': autores_objs[0]},
        {'titulo': 'El Amor en los Tiempos del Cólera', 'cat': 'Romance', 'autor': autores_objs[0]},
        {'titulo': 'La Casa de los Espíritus', 'cat': 'Realismo Mágico', 'autor': autores_objs[1]},
        {'titulo': 'Harry Potter y la Piedra Filosofal', 'cat': 'Fantasía', 'autor': autores_objs[2]},
    ]

    for data in libros_data:
        Libro.objects.get_or_create(
            titulo=data['titulo'],
            defaults={
                'autor': data['autor'],
                'categoria': data['cat'],
                'estado': 'disponible'
            }
        )
    print(f"✅ {len(libros_data)} Libros verificados/creados.")

    # --- 5. ESCENARIO DE PRUEBA DE MULTA (Opcional) ---
    # Creamos una situación donde Okarin YA pidió un libro y se atrasó.
    # Esto te sirve para probar el botón de multa DIRECTAMENTE.
    
    print("\n--- Generando Escenario de Prueba de Multa ---")
    libro_multa = Libro.objects.filter(titulo='Harry Potter y la Piedra Filosofal').first()
    
    if libro_multa and libro_multa.estado == 'disponible':
        # 1. Crear Solicitud Aprobada antigua
        solicitud = SolicitudPrestamo.objects.create(
            socio=socio_okarin,
            libro=libro_multa,
            estado='aprobado'
        )
        
        # 2. Crear Préstamo con fecha pasada (hace 10 días)
        hace_10_dias = timezone.now() - timedelta(days=10)
        prestamo = Prestamo.objects.create(
            solicitud=solicitud,
            fecha_prestamo=hace_10_dias,
            fecha_devolucion_esperada=hace_10_dias + timedelta(days=7) # Debió devolverlo hace 3 días
        )
        
        # 3. Marcar libro como prestado
        libro_multa.estado = 'prestado'
        libro_multa.save()
        
        print("⚠️ ESCENARIO CREADO: Okarin tiene 'Harry Potter' vencido hace 3 días.")
        print("   -> Ve al panel de Bibliotecario y dale a 'Devolver' para ver la multa.")
    else:
        print("ℹ️ El escenario de multa ya existe o el libro no está disponible.")

    print("\n🚀 ¡Población de datos finalizada con éxito!")

if __name__ == '__main__':
    poblar_datos()