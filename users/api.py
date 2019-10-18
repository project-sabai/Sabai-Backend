import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

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
        username = request.POST['username']
        password = request.POST['password']
        title = request.POST['title']
        name = request.POST['name']

        print('checkpoint: can get information')

        user = User.objects.create_user(username, None, password)
        user.first_name = title
        user.last_name = name

        user.save()

        return JsonResponse({"message": 'success'}, status=200)
    except Exception as e:
        print('error is ', e)
        return JsonResponse({"message": str(e)}, status=400)

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

@api_view(['GET'])
def get_details(request):
    try:
        users = User.objects.all()
        response = serializers.serialize("json", users)
        return HttpResponse(response, content_type="application/json")
    except Exception as e:
        print('error is ', e)

