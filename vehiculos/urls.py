from django.urls import path
from . import views

urlpatterns = [
    path("vehiculos/", views.vehiculo_list_create, name="vehiculo_list_create"),
    path("vehiculos/<int:vehiculo_id>/", views.vehiculo_detail, name="vehiculo_detail"),
    path("reparaciones/costo-total", views.costo_total_reparaciones, name="costo_total_reparaciones"),
    path("vehiculos/cambio-aceite", views.cambio_aceite, name="cambio_aceite"),
]
