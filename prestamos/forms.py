from django import forms
from .models import SolicitudPrestamo

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudPrestamo
        fields = ['libro']
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-control', 'id': 'select-libro'})
        }

    def clean_libro(self):
        """Validación de seguridad OWASP: Integridad de datos"""
        libro = self.cleaned_data.get('libro')
        if libro.estado != 'disponible':
            raise forms.ValidationError(f"El libro '{libro.titulo}' ya no está disponible.")
        return libro