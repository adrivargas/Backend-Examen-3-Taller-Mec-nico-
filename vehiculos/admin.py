from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "placa",
        "marca",
        "modelo",
        "anio",
        "color",
        "tipo",
        "kilometraje",
        "nombre_propietario",
        "telefono_propietario",
        "estado",
    )
    search_fields = ("placa", "marca", "modelo", "nombre_propietario")
