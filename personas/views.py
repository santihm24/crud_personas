from django.shortcuts import render, redirect # importar render y redirect
from .models import Persona # importar el modelo Persona
from .forms import PersonaForm # importar el formulario PersonaForm

# Create your views here.

def lista_personas(request):  # función para listar personas
    personas = Persona.objects.all()   # obtener todas las personas de la base de datos
    return render(request, 'personas/lista.html', {'personas': personas})   # renderizar la plantilla lista.html con el contexto de personas

def crear_persona(request):  # función para crear una nueva persona
    if request.method == 'POST':  # si el método de la solicitud es POST
        form = PersonaForm(request.POST)  # crear una instancia del formulario con los datos de la solicitud
        if form.is_valid():  # si el formulario es válido
            form.save()  # guardar la nueva persona en la base de datos  
            return redirect('lista_personas')  # redirigir a la lista de personas
    else:       # si el método de la solicitud no es POST
        form = PersonaForm()        # crear una instancia vacía del formulario
        return render(request, 'personas/formulario.html', {'form': form})    # renderizar la plantilla formulario.html con el contexto del formulario
     
def editar_persona(request, id):     # funcion para editar persona ya creada
        persona = Persona.objects.get(id=id) # obtener la persona por su id
        if request.method == 'POST': # si el método de la solicitud es POST
            form = PersonaForm(request.POST, instance=persona) # crear una instancia del formulario con los datos de la solicitud y la persona a editar
            if form.is_valid(): # si el formulario es válido
                form.save() # guardar los cambios en la base de datos
                return redirect('lista_personas') # redirigir a la lista de personas
        else: 
            form = PersonaForm(instance=persona) # si el método de la solicitud no es POST, crear una instancia del formulario con la persona a editar
            return render(request, 'personas/formulario.html', {'form': form})  # renderizar la plantilla formulario.html con el contexto del formulario
        
def eliminar_persona(request, id):   # funcion para eliminar persona
    persona = Persona.objects.get(id=id)  # obtener la persona por su id
    persona.delete()  # eliminar la persona de la base de datos
    return redirect('lista_personas') # redirigir a la lista de personas
