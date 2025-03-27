from django.shortcuts import render, redirect
from .models import Persona
from .forms import PersonaForm

# Create your views here.

def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'personas/lista.html', {'personas': personas})

def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_personas')
    else:
        form = PersonaForm()
        return render(request, 'personas/formulario.html', {'form': form})
    
def editar_persona(request, id):
        persona = Persona.objects.get(id=id)
        if request.method == 'POST':
            form = PersonaForm(request.POST, instance=persona)
            if form.is_valid():
                form.save()
                return redirect('lista_personas')
        else:
            form = PersonaForm(instance=persona)
            return render(request, 'personas/formulario.html', {'form': form})
        
def eliminar_persona(request, id):
    persona = Persona.objects.get(id=id)
    persona.delete()
    return redirect('lista_personas')
