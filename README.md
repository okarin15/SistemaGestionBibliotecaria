# Sistema de Gestión Bibliotecaria (SGB)

**Versión:** 1.0.0 - Release Candidate
**Evaluación:** Ingeniería de Software - Entrega Final

Sistema integral para la administración de préstamos, inventario y usuarios de una biblioteca comunitaria. Desarrollado bajo estándares de seguridad OWASP Top 10, cumplimiento normativo ISO/IEC 27000 y arquitectura MVT de Django.

---

## Características Principales

* **Gestión de Préstamos:** Flujo completo de Solicitud, Aprobación, Préstamo y Devolución.
* **Cálculo Automatizado de Multas:** Algoritmo que detecta retrasos en tiempo real y aplica sanciones monetarias ($1.000 CLP/día).
* **Seguridad Endurecida (Hardening):**
    * Validación de entrada robusta mediante Django Forms (Mitigación OWASP Injection).
    * Protección CSRF y Decoradores de control de acceso (@login_required).
* **Experiencia de Usuario (UX):** Alertas visuales con etiquetas de estado para gestión de deudas.

---

## Stack Tecnológico

* **Backend:** Python 3.10+ / Django 5.x
* **Frontend:** Bootstrap 5 + Tailwind CSS (Componentes dinámicos).
* **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Producción).
* **Testing:** Unittest (Pruebas automatizadas de lógica de negocio).

---

## Guía de Instalación y Ejecución

Sigue estos pasos para desplegar el proyecto en local:

1.  **Clonar el repositorio:**
    git clone [TU_LINK_DEL_REPO_AQUI]
    cd [NOMBRE_DE_LA_CARPETA]

2.  **Crear y activar entorno virtual:**
    python -m venv venv
    
    # En Windows:
    venv\Scripts\activate
    
    # En Mac/Linux:
    source venv/bin/activate

3.  **Instalar dependencias:**
    pip install -r requirements.txt

4.  **Aplicar migraciones:**
    python manage.py migrate

5.  **IMPORTANTE: Cargar Datos de Prueba (Script de Población):**
    Este script crea automáticamente los usuarios, libros y genera un escenario de multa (préstamo atrasado) para validar la lógica de negocio sin esperar días reales.
    
    python populate.py

6.  **Iniciar el servidor:**
    (Usamos --insecure para forzar la carga de estilos estáticos si DEBUG=False)
    
    python manage.py runserver --insecure

---

## Credenciales de Acceso

El script populate.py genera las siguientes cuentas para pruebas:

| Rol | Usuario | Contraseña | Funcionalidad a Probar |
| :--- | :--- | :--- | :--- |
| Bibliotecario | admin | biblioteca1234 | Aprobar solicitudes, Registrar devoluciones (ver multas). |
| Socio | okarin | biblioteca1234 | Solicitar libros, Ver historial y etiquetas de atraso. |

---

## Ejecución de Pruebas Automatizadas (QA)

Para validar la integridad del cálculo de multas y la lógica de seguridad, ejecutar el suite de tests:

python manage.py test prestamos

Resultado esperado: "Ran 1 test in 0.0xxs ... OK"

---

## Licencia y Normativa
Proyecto académico desarrollado conforme a los criterios de evaluación de Ingeniería de Software.