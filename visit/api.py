from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json

from clinicmodels.models import Patient, Visit
from visit.forms import VisitForm


@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        patient_id = data['patient']
        # patient_id = request.POST['patient']
        
        # check if patient exists
        # error will be raised if it does not exist
        patient = Patient.objects.get(pk=patient_id)

        print('this is the data ', data)

        # if len(consultations) == 0:
        #     return JsonResponse({"message": "Patient should have at least one consultation"}, status=400)

        # if all is good, proceed to save data
        print('checkpoint! all good.')
        visit_form = VisitForm(data)
        if visit_form.is_valid():
            print('proceeding to save')

            visit  = visit_form.save()

            response = serializers.serialize("json", [visit, ])
            return HttpResponse(response, content_type='application/json')

        else:
            print(visit_form.errors)
            return JsonResponse(visit_form.errors, status=400)
       
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['POST'])
@csrf_exempt
def migrate(request):
    try:
        data = request.POST.copy()
        patient_id = data['patient']
        # patient_id = request.POST['patient']
        
        # check if patient exists
        # error will be raised if it does not exist
        patient = Patient.objects.get(pk=patient_id)

        print('this is the data ', data)

        # if len(consultations) == 0:
        #     return JsonResponse({"message": "Patient should have at least one consultation"}, status=400)

        # if all is good, proceed to save data
        print('checkpoint! all good.')
        visit_form = VisitForm(data)
        if visit_form.is_valid():
            print('proceeding to save')

            visit  = visit_form.save()

            response = serializers.serialize("json", [visit, ])
            return HttpResponse(response, content_type='application/json')

        else:
            print(visit_form.errors)
            return JsonResponse(visit_form.errors, status=400)
       
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def get_details(request):
    try:
        sort_params = request.GET.dict()
        visits = Visit.objects.filter(**sort_params)

        response = serializers.serialize('json', visits)

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
        visit = Visit.objects.filter(**sort_params)

        # updating row and saving changes to DB
        data = json.loads(request.body.decode('utf-8'))
        visit.update(**data)

        return JsonResponse({
            "message": "success"
        }, status = 200)

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)









