from django.shortcuts import render, redirect  # Importar render y redirect
from .models import Persona  # Importar el modelo Persona
from .forms import PersonaForm  # Importar el formulario de Persona
from crud_personas.firebase_config import get_firebase_db  # Importar la función de configuración de Firebase

# Función para listar personas
def lista_personas(request):
    personas = Persona.objects.all()  # Obtener todas las personas de la base de datos local (PostgreSQL)
    return render(request, 'personas/lista.html', {'personas': personas})  # Renderizar la plantilla con la lista de personas

# Función para crear una nueva persona
def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():      # Validar el formulario
            # Guardar la persona en la base de datos local
            nueva_persona = form.save()

            firebase_db = get_firebase_db()

            # Sincronizar con Firebase
            firebase_result = firebase_db.child('personas').push({
            'nombre': nueva_persona.nombre,
            'apellido': nueva_persona.apellido,
            'edad': nueva_persona.edad
})

            # Guardar la clave de Firebase en la base de datos local (en PostgreSQL)
            firebase_key = firebase_result['name']
            nueva_persona.firebase_key = firebase_key  # 'name' es la clave generada por Firebase
            nueva_persona.save()

            return redirect('lista_personas')
    else:
        form = PersonaForm()
    return render(request, 'personas/formulario.html', {'form': form})


def editar_persona(request, id):
    try:
        persona = Persona.objects.get(id=id)  # Obtener la persona desde la base de datos local
    except Persona.DoesNotExist:
        return redirect('lista_personas')  # Redirigir si la persona no existe

    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            persona_editada = form.save()  # Guardar los cambios en la base de datos local

            firebase_db = get_firebase_db()

            # Sincronizar con Firebase (actualizar el nodo correspondiente)
            # ⚠️ Usar la clave de Firebase, no el ID local
            firebase_db.child('personas').child(persona.firebase_key).update({
            'nombre': persona_editada.nombre,
            'apellido': persona_editada.apellido,
            'edad': persona_editada.edad
})


            return redirect('lista_personas')
    else:
        form = PersonaForm(instance=persona)

    return render(request, 'personas/formulario.html', {'form': form})


# Función para eliminar una persona
def eliminar_persona(request, id):
    try:
        # Obtener la persona por su ID desde la base de datos local (PostgreSQL)
        persona = Persona.objects.get(id=id)
        
        # Eliminar la persona desde la base de datos local
        persona.delete()

        # Eliminar la persona desde Firebase
        firebase_db = get_firebase_db()

        # Verifica que la referencia al ID de Firebase sea correcta
        print(f"Eliminando el registro de Firebase con la clave: {persona.firebase_key}")

        # Eliminar el registro en Firebase usando la clave generada automáticamente por Firebase
        firebase_db.child('personas').child(persona.firebase_key).remove()

        return redirect('lista_personas')
    
    except Persona.DoesNotExist:
        # Si la persona no existe en la base de datos local, redirigir a la lista de personas
        return redirect('lista_personas')
    except Exception as e:
        # Capturar cualquier excepción y mostrar un mensaje de error
        print(f"Error al eliminar la persona: {e}")
        return redirect('lista_personas')  # Redirigir en caso de error

