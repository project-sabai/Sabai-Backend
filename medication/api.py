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
        sort_params = request.GET.dict()
        medications = Medication.objects.filter(**sort_params)

        response = serializers.serialize('json', medications)

        return HttpResponse(response, content_type="application/json")
    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)

@api_view(['PATCH'])
def update_details(request):
    try:
        # finding row to update
        sort_params = request.query_params.dict()
        medication = Medication.objects.filter(**sort_params)

        # updating row and saving changes to DB
        data = json.loads(request.body.decode('utf-8'))
        medication.update(**data)

        return JsonResponse({
            "message": "success"
        }, status = 200)

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)