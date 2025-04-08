"""
URL configuration for crud_personas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Importa admin desde django.contrib
from django.urls import path, include # Importa include para incluir otras URLconf
from django.shortcuts import redirect  # Importa redirect
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls), # URL para el panel de administración
    path('personas/', include('personas.urls')), # Incluye las URLs de la aplicación personas
    path('', lambda request: redirect('lista_personas')),  # Redirige la raíz a lista_personas
]

if settings.DEBUG: 
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  # URL para el panel de depuración
    ] + urlpatterns  # Agrega las URLs de depuración a las URLs principales
     
