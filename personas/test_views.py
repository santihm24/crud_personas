from django.test import TestCase, Client
from django.urls import reverse
from personas.models import Persona
from personas.forms import PersonaForm

class EditarPersonaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.persona = Persona.objects.create(nombre="Juan", apellido="Perez", edad=30)
        self.editar_url = reverse('editar_persona', args=[self.persona.id])

    def test_editar_persona_get(self):
        response = self.client.get(self.editar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personas/formulario.html')
        self.assertIsInstance(response.context['form'], PersonaForm)
        self.assertEqual(response.context['form'].instance, self.persona)

    def test_editar_persona_post_valid_data(self):
        data = {
            'nombre': 'Carlos',
            'apellido': 'Lopez',
            'edad': 35
        }
        response = self.client.post(self.editar_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful edit
        self.assertRedirects(response, reverse('lista_personas'))
        self.persona.refresh_from_db()
        self.assertEqual(self.persona.nombre, 'Carlos')
        self.assertEqual(self.persona.apellido, 'Lopez')
        self.assertEqual(self.persona.edad, 35)

    def test_editar_persona_post_invalid_data(self):
        data = {
            'nombre': '',  # Invalid data (empty name)
            'apellido': 'Lopez',
            'edad': 35
        }
        response = self.client.post(self.editar_url, data)
        self.assertEqual(response.status_code, 200)  # Re-render the form
        self.assertTemplateUsed(response, 'personas/formulario.html')
        self.assertIsInstance(response.context['form'], PersonaForm)
        self.assertTrue(response.context['form'].errors)
        self.persona.refresh_from_db()
        self.assertNotEqual(self.persona.nombre, '')  # Ensure the data was not updated