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

@api_view(['GET'])
def get_details(request):
    try:
        sort_params = request.GET.dict()
        users = User.objects.filter(**sort_params)

        response = serializers.serialize('json', users)

        return HttpResponse(response, content_type="application/json")

    except Exception as e:
        print('error is ', e)
        return JsonResponse({
            "message": str(e)
        }, status = 400)

