from django.db import models   # Importa el módulo models de Django

# Create your models here.

class Persona(models.Model):  # Define el modelo Persona
    nombre = models.CharField(max_length=100)  # Campo de texto para el nombre
    apellido = models.CharField(max_length=100)  # Campo de texto para el apellido
    edad = models.IntegerField()  # Campo entero para la edad
    firebase_key = models.CharField(max_length=255, null=True, blank=True)  # Campo para guardar la clave de Firebase


    def __str__(self):     # Método para representar el objeto como una cadena
        return f"{self.nombre} {self.apellido}"    # Devuelve el nombre y apellido de la persona como una cadena
    