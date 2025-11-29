# Sistema de Gestión Bibliotecaria (SGB)

Prototipo de software diseñado para la modernización de los procesos de préstamo y control de inventario en bibliotecas. Este proyecto fue desarrollado como parte de la **Evaluación 3 de Ingeniería de Software**, enfocándose en una arquitectura escalable, segura y eficiente.

## 🚀 Descripción del Proyecto

El **SGB** es una aplicación web basada en el patrón **MVT (Modelo-Vista-Template)** que permite a los administradores gestionar el ciclo de vida de los recursos bibliográficos. El sistema soluciona la problemática de la gestión manual, ofreciendo trazabilidad en los préstamos y una base de datos normalizada.

### Funcionalidades Principales
- **Gestión de Inventario:** Registro de Libros con vinculación a Autores (Relación 1:N).
- **Control de Autores:** Base de datos independiente para autores, evitando redundancia.
- **Flujo de Préstamos:** Solicitud, aprobación y seguimiento de devoluciones.
- **Interfaz Responsiva:** Diseño adaptativo utilizando **Bootstrap 5**.
- **Seguridad:** Protección contra ataques CSRF e Inyección SQL (OWASP).

## 🛠️ Tecnologías Utilizadas

Este proyecto ha sido construido utilizando un stack tecnológico moderno y orientado a la nube (SaaS):

* **Backend:** Python 3.10+, Django Framework 4.x
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Base de Datos:** SQLite (Entorno de desarrollo)
* **Control de Versiones:** Git & GitHub
* **Editor de Código:** Visual Studio Code

## ⚙️ Instalación y Despliegue Local

Para ejecutar este proyecto en tu máquina local, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git](https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git)
    cd NOMBRE_DEL_REPO
    ```

2.  **Crear y activar un entorno virtual (Opcional pero recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install django
    ```

4.  **Ejecutar migraciones de base de datos:**
    ```bash
    python manage.py migrate
    ```

5.  **Iniciar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

6.  **Acceder al sistema:**
    Abre tu navegador en: `http://127.0.0.1:8000/`

## 📄 Estructura del Proyecto

- `biblioteca/`: Configuración principal del proyecto (Settings, URLs centrales).
- `prestamos/`: Aplicación central que contiene la lógica de negocio (Models, Views).
- `templates/`: Archivos HTML y plantillas base (Frontend).
- `manage.py`: Utilidad de línea de comandos de Django.

## 👥 Autor
Desarrollado para la asignatura de Ingeniería de Software.