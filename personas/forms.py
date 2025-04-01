from django import forms  # importar forms
from .models import Persona   # importar el modelo Persona

class PersonaForm(forms.ModelForm):   # crear un formulario basado en el modelo Persona
    class Meta:        # clase interna Meta para definir la configuración del formulario
        model = Persona        # especificar el modelo a usar
        fields = ['nombre', 'apellido', 'edad']   # especificar los campos a incluir en el formulario