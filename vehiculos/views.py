import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Vehiculo

def parse_json(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except Exception:
        return {}

@csrf_exempt
def vehiculo_list_create(request):
    if request.method == "GET":
        vehiculos = list(
            Vehiculo.objects.values(
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
        )
        return JsonResponse(
            {
                "message": "Listado de vehículos obtenido correctamente.",
                "data": vehiculos,
            },
            status=200,
        )

    if request.method == "POST":
        data = parse_json(request)
        required = [
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
        ]
        missing = [f for f in required if f not in data]
        if missing:
            return JsonResponse(
                {"message": "Faltan campos requeridos.", "missing_fields": missing},
                status=400,
            )

        vehiculo = Vehiculo.objects.create(
            placa=data["placa"],
            marca=data["marca"],
            modelo=data["modelo"],
            anio=data["anio"],
            color=data["color"],
            tipo=data["tipo"],
            kilometraje=data["kilometraje"],
            nombre_propietario=data["nombre_propietario"],
            telefono_propietario=data["telefono_propietario"],
            estado=data["estado"],
        )

        return JsonResponse(
            {
                "message": "Vehículo creado correctamente.",
                "data": {
                    "id": vehiculo.id,
                    "placa": vehiculo.placa,
                    "marca": vehiculo.marca,
                    "modelo": vehiculo.modelo,
                    "anio": vehiculo.anio,
                    "color": vehiculo.color,
                    "tipo": vehiculo.tipo,
                    "kilometraje": vehiculo.kilometraje,
                    "nombre_propietario": vehiculo.nombre_propietario,
                    "telefono_propietario": vehiculo.telefono_propietario,
                    "estado": vehiculo.estado,
                },
            },
            status=201,
        )

    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def vehiculo_detail(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == "GET":
        data = {
            "id": vehiculo.id,
            "placa": vehiculo.placa,
            "marca": vehiculo.marca,
            "modelo": vehiculo.modelo,
            "anio": vehiculo.anio,
            "color": vehiculo.color,
            "tipo": vehiculo.tipo,
            "kilometraje": vehiculo.kilometraje,
            "nombre_propietario": vehiculo.nombre_propietario,
            "telefono_propietario": vehiculo.telefono_propietario,
            "estado": vehiculo.estado,
        }
        return JsonResponse(
            {"message": "Detalle del vehículo obtenido correctamente.", "data": data},
            status=200,
        )

    if request.method in ["PUT", "PATCH"]:
        data = parse_json(request)
        for field in [
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
        ]:
            if field in data:
                setattr(vehiculo, field, data[field])
        vehiculo.save()

        updated = {
            "id": vehiculo.id,
            "placa": vehiculo.placa,
            "marca": vehiculo.marca,
            "modelo": vehiculo.modelo,
            "anio": vehiculo.anio,
            "color": vehiculo.color,
            "tipo": vehiculo.tipo,
            "kilometraje": vehiculo.kilometraje,
            "nombre_propietario": vehiculo.nombre_propietario,
            "telefono_propietario": vehiculo.telefono_propietario,
            "estado": vehiculo.estado,
        }
        return JsonResponse(
            {"message": "Vehículo actualizado correctamente.", "data": updated},
            status=200,
        )

    if request.method == "DELETE":
        vehiculo.delete()
        return JsonResponse(
            {"message": "Vehículo eliminado correctamente."},
            status=200,
        )

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])

@csrf_exempt
def costo_total_reparaciones(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = parse_json(request)
    costos = data.get("costos")

    if not isinstance(costos, list):
        return JsonResponse(
            {"message": "El campo 'costos' debe ser un arreglo de números."},
            status=400,
        )

    total = 0
    for c in costos:  # ciclo sobre el arreglo
        try:
            total += float(c)
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    "message": "Todos los elementos de 'costos' deben ser numéricos.",
                },
                status=400,
            )

    if total < 100:
        mensaje = "Reparación económica"
    elif 100 <= total <= 500:
        mensaje = "Reparación media"
    else:
        mensaje = "Reparación costosa"

    return JsonResponse(
        {
            "message": "Costo total calculado correctamente.",
            "total": total,
            "categoria": mensaje,
        },
        status=200,
    )

@csrf_exempt
def cambio_aceite(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = parse_json(request)
    km_actual = data.get("km_actual")
    km_ultimo_cambio = data.get("km_ultimo_cambio")

    if km_actual is None or km_ultimo_cambio is None:
        return JsonResponse(
            {"message": "Se requieren 'km_actual' y 'km_ultimo_cambio'."},
            status=400,
        )

    try:
        km_actual = float(km_actual)
        km_ultimo_cambio = float(km_ultimo_cambio)
    except (TypeError, ValueError):
        return JsonResponse(
            {
                "message": "Los valores de 'km_actual' y 'km_ultimo_cambio' deben ser numéricos.",
            },
            status=400,
        )

    km_recorridos = km_actual - km_ultimo_cambio

    if km_recorridos < 5000:
        recomendacion = "No es necesario cambio inmediato"
    elif 5000 <= km_recorridos <= 8000:
        recomendacion = "Recomendable programar cambio"
    else:
        recomendacion = "Cambio urgente de aceite"

    return JsonResponse(
        {
            "message": "Evaluación de cambio de aceite realizada.",
            "km_recorridos": km_recorridos,
            "recomendacion": recomendacion,
        },
        status=200,
    )
