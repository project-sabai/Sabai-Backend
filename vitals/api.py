from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Vitals
from vitals.forms import VitalsForm


@api_view(['POST'])
@csrf_exempt
def create_new_vitals(request):
    try:
        form = VitalsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.save()
            response = serializers.serialize("json", [vitals, ])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_vitals_by_id(request):
    try:
        if 'id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
        vitals_id = request.GET['id']
        vitals = Vitals.objects.get(pk=vitals_id)
        response = serializers.serialize("json", [vitals, ])
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def get_vitals_by_visit(request):
    try:
        if 'visit_id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'visit_id' not found"}, status=400)
        visit_id = request.GET['visit_id']
        vitals = Vitals.objects.filter(visit=visit_id)
        response = serializers.serialize("json", vitals)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_vitals_by_patient(request):
    try:
        if 'patient_id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'patient_id' not found"}, status=400)
        patient_id = request.GET['patient_id']
        vitals = Vitals.objects.filter(visit__patient_id=patient_id)
        response = serializers.serialize("json", vitals)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)
