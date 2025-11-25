from django.db import models


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.IntegerField()
    color = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    kilometraje = models.IntegerField()
    nombre_propietario = models.CharField(max_length=150)
    telefono_propietario = models.CharField(max_length=20)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
