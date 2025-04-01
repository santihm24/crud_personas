from django.urls import path   # Importa path
from . import views # Importa views desde el mismo directorio

# Define la lista de URL patterns para la aplicación personas
urlpatterns = [        
    path('', views.lista_personas, name='lista_personas'), # URL para la lista de personas
    path('crear/', views.crear_persona, name='crear_persona'), # URL para crear una nueva persona
    path('editar/<int:id>/', views.editar_persona, name='editar_persona'),  # URL para editar una persona existente
    path('eliminar/<int:id>/', views.eliminar_persona, name='eliminar_persona'),    # URL para eliminar una persona  
]