from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_datetime

from clinicmodels.models import Visit, Consult
from consult.forms import ConsultForm

import json

@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        consult_form = ConsultForm(data)

        if consult_form.is_valid():
            consult = consult_form.save()
            response = serializers.serialize("json", [consult, ])
            
            return HttpResponse(response, content_type='application/json')
        else:
            print('failing')
            print(consult_form.errors)
            return JsonResponse({"message": consult_form.errors}, status=400)
    except ObjectDoesNotExist as e:
        print('this is the error ', e)
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['POST'])
@csrf_exempt
def migrate(request):
    try:
        data = request.POST.copy()
        consult_form = ConsultForm(data)

        if consult_form.is_valid():
            consult = consult_form.save()
            response = serializers.serialize("json", [consult, ])
            
            return HttpResponse(response, content_type='application/json')
        else:
            print('failing')
            print(consult_form.errors)
            return JsonResponse({"message": consult_form.errors}, status=400)
    except ObjectDoesNotExist as e:
        print('this is the error ', e)
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def get_details(request):
    try:
        sort_params = request.GET.dict()
        consults = Consult.objects.filter(**sort_params)

        response = serializers.serialize('json', consults)

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
        consult = Consult.objects.filter(**sort_params)

        # updating row and saving changes to DB
        data = json.loads(request.body.decode('utf-8'))
        consult.update(**data)

        return JsonResponse({
            "message": "success"
        }, status = 200)

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)

