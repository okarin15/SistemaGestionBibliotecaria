from django.test import TestCase
from .models import Libro, Autor

class PrestamoTestCase(TestCase):
    def setUp(self):
        # Creamos un autor de prueba para validar la relación
        self.autor = Autor.objects.create(nombre="Gabriel", apellido="Garcia", nacionalidad="Colombiana")

    def test_creacion_libro(self):
        """Prueba unitaria para validar el registro correcto de un libro"""
        libro = Libro.objects.create(
            titulo="Cien Años de Soledad",
            autor=self.autor,
            categoria="Novela",
            estado="disponible"
        )
        # Verificamos que se guardó correctamente
        self.assertEqual(libro.titulo, "Cien Años de Soledad")
        self.assertEqual(libro.estado, "disponible")
