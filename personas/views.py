from django.shortcuts import render, redirect
from .models import Persona
from .forms import PersonaForm
from crud_personas.firebase_config import get_firebase_db  # Importar la función de configuración de Firebase

# Función para listar personas
def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'personas/lista.html', {'personas': personas})

# Función para crear una nueva persona
def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            # Guardar la persona en la base de datos local
            nueva_persona = form.save()

            # Sincronizar con Firebase
            firebase_db = get_firebase_db()
            firebase_db.push({
                'nombre': nueva_persona.nombre,
                'apellido': nueva_persona.apellido,
                'edad': nueva_persona.edad
            })

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

            # Sincronizar con Firebase (actualizar el nodo correspondiente)
            firebase_db = get_firebase_db()
            firebase_db.child(str(persona.id)).update({
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
        # Obtener la persona desde la base de datos local
        persona = Persona.objects.get(id=id)
        persona.delete()  # Eliminar la persona de la base de datos local

        # Eliminar desde Firebase
        firebase_db = get_firebase_db()
        firebase_db.child(str(id)).remove()  # Eliminar de Firebase usando el id como cadena
    except Persona.DoesNotExist:
        return redirect('lista_personas')  # Redirigir si la persona no existe

    return redirect('lista_personas')  # Redirigir a la lista de personas después de la eliminación

