import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import MedicalVitals, Visit
from medicalvitals.forms import MedicalVitalsForm

from clinicmodels.models import Medication
from medication.forms import MedicationForm

# Remember
# Create
# Read
# Updated
# Delete

@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        print(request.POST)
        form = MedicationForm(request.POST)
        print('form is valid? ', form.is_valid())
        print(form.errors)
        if form.is_valid():
            medication = form.save(commit=False)
            print('this is medication ', medication)
            medication.save()
            response = serializers.serialize("json", [medication])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def get_details(request):
    try:
        medications = Medication.objects.all()
        response = serializers.serialize("json", medications)
        return HttpResponse(response, content_type="application/json")
    except Exception as e:
        print('error is ', e)


@api_view(['POST'])
@csrf_exempt
def update_vitals(request):
    try:
        if 'id' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'id' not found"}, status=400)
        vitals_id = request.POST['id']
        vitals = MedicalVitals.objects.get(pk=vitals_id)
        if 'height' in request.POST:
            vitals.height = request.POST['height']
        if 'weight' in request.POST:
            vitals.weight = request.POST['weight']
        if 'systolic' in request.POST:
            vitals.systolic = request.POST['systolic']
        if 'diastolic' in request.POST:
            vitals.diastolic = request.POST['diastolic']
        if 'temperature' in request.POST:
            vitals.temperature = request.POST['temperature']
        if 'hiv_positive' in request.POST:
            hiv = request.POST['hiv_positive']
            if hiv == "true":
                hiv = True
            elif hiv == "false":
                hiv = False
            vitals.hiv_positive = hiv
        if 'ptb_positive' in request.POST:
            ptb = request.POST['ptb_positive']
            if ptb == "true":
                ptb = True
            elif ptb == "false":
                ptb = False
            vitals.ptb_positive = ptb
        if 'hepc_positive' in request.POST:
            hepc = request.POST['hepc_positive']
            if hepc == "true":
                hepc = True
            elif hepc == "false":
                hepc = False
            vitals.hepc_positive = hepc
        if 'heart_rate' in request.POST:
            vitals.heart_rate = request.POST['heart_rate']
        vitals.save()
        response = serializers.serialize("json", [vitals, ])
        return HttpResponse(response, content_type='application/json')

    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message", str(e)}, status=400)
    except TypeError as e:
        return JsonResponse({"message", str(e)}, status=400)


