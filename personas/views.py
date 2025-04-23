from django.shortcuts import render, redirect
from .models import Persona
from .forms import PersonaForm
from crud_personas.firebase_config import get_firebase_db


def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'personas/lista.html', {'personas': personas})


def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            nueva_persona = form.save()
            firebase_db = get_firebase_db()

            try:
                firebase_result = firebase_db.child('personas').push({
                    'nombre': str(nueva_persona.nombre),
                    'apellido': str(nueva_persona.apellido),
                    'edad': int(nueva_persona.edad)
                })

                firebase_key = firebase_result.get('name')
                if firebase_key:
                    nueva_persona.firebase_key = firebase_key
                    nueva_persona.save()
                else:
                    print("No se obtuvo clave de Firebase")

            except Exception as e:
                print(f"Error al sincronizar con Firebase: {e}")

            return redirect('lista_personas')
    else:
        form = PersonaForm()
    return render(request, 'personas/formulario.html', {'form': form})


def editar_persona(request, id):
    try:
        persona = Persona.objects.get(id=id)
    except Persona.DoesNotExist:
        return redirect('lista_personas')

    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            persona_editada = form.save()
            firebase_db = get_firebase_db()

            if persona.firebase_key:
                try:
                    firebase_db.child('personas').child(persona.firebase_key).update({
                        'nombre': str(persona_editada.nombre),
                        'apellido': str(persona_editada.apellido),
                        'edad': int(persona_editada.edad)
                    })
                except Exception as e:
                    print(f"Error al actualizar en Firebase: {e}")
            else:
                print("⚠️ Esta persona no tiene clave de Firebase.")

            return redirect('lista_personas')
    else:
        form = PersonaForm(instance=persona)

    return render(request, 'personas/formulario.html', {'form': form})


def eliminar_persona(request, id):
    try:
        persona = Persona.objects.get(id=id)

        firebase_key = persona.firebase_key

        persona.delete()

        if firebase_key:
            try:
                firebase_db = get_firebase_db()
                firebase_db.child('personas').child(firebase_key).remove()
                print(f"✔️ Registro eliminado en Firebase con clave: {firebase_key}")
            except Exception as e:
                print(f"Error al eliminar en Firebase: {e}")
        else:
            print("⚠️ Esta persona no tenía clave de Firebase.")

        return redirect('lista_personas')

    except Persona.DoesNotExist:
        return redirect('lista_personas')
    except Exception as e:
        print(f"Error inesperado al eliminar persona: {e}")
        return redirect('lista_personas')
