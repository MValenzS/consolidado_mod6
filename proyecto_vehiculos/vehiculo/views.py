from django.shortcuts import render, redirect
from .forms import VehiculoForm
from .models import Vehiculo
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


# Vista para agregar un vehículo
@login_required
@permission_required('vehiculo.add_vehiculo', raise_exception=True)
def agregar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehiculo agregado con exito')
            return redirect('index')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculo/agregar_vehiculo.html', {'form': form})

# Vista para la página de inicio
def index(request):
    return render(request, 'vehiculo/index.html')

# Vista para listar vehículos con categorías de precios
@login_required
@permission_required('vehiculo.visualizar_catalogo', raise_exception=True)
def listar_vehiculos(request):
    # Consulta todos los vehículos de la base de datos
    vehiculos = Vehiculo.objects.all()

    # Procesa la condición de precio y organiza los datos
    vehiculos_list = []
    for vehiculo in vehiculos:
        if vehiculo.precio is not None:  # Asegurarse de que el precio no sea nulo
            if vehiculo.precio <= 10000:
                condicion_precio = 'Bajo'
            elif 10001 <= vehiculo.precio <= 50000:
                condicion_precio = 'Medio'
            else:
                condicion_precio = 'Alto'
        else:
            condicion_precio = 'Desconocido'  # Si el precio es None

        vehiculos_list.append({
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'serial_carroceria': vehiculo.serial_carroceria,
            'serial_motor': vehiculo.serial_motor,
            'categoria': vehiculo.categoria,
            'precio': vehiculo.precio,
            'condicion_precio': condicion_precio
        })

    # Envía la lista de vehículos al template
    return render(request, 'vehiculo/listar_vehiculos.html', {'vehiculos_list': vehiculos_list})
