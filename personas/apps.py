from django.apps import AppConfig  # Importa AppConfig desde django.apps


class PersonasConfig(AppConfig):  # Define la clase de configuración de la aplicación
    default_auto_field = 'django.db.models.BigAutoField'  # Define el tipo de campo automático por defecto
    name = 'personas'  # Nombre de la aplicación
