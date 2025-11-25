import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Vehiculo


def parse_json_body(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = {}
    return data


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
        data = parse_json_body(request)

        required_fields = [
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

        missing = [f for f in required_fields if f not in data]
        if missing:
            return JsonResponse(
                {
                    "message": "Faltan campos requeridos.",
                    "missing_fields": missing,
                },
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
        data = parse_json_body(request)
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


