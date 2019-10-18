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

@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        consult_form = ConsultForm(request.POST)




        if consult_form.is_valid():
            # print('this is the consult_form ', consult_form)
            # consult_form.consult_date = request.POST['consult_date']
            # print('doneso ', consult_form )
            consult = consult_form.save()
            response = serializers.serialize("json", [consult, ])
            
            return HttpResponse(response, content_type='application/json')
        else:
            return JsonResponse({"message": consult_form.errors}, status=400)
    except ObjectDoesNotExist as e:
        print('this is the error ', e)
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def get_consults(request):
    try:
        sort_params = request.GET.dict()
        consults = Consult.objects.filter(**sort_params)
        response = serializers.serialize('json', consults)
        return HttpResponse(response, content_type="application/json")

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)

# @api_view(['POST'])
# def create_new_consult_type(request):
#     try:
#         if 'consult_type' not in request.POST:
#             return JsonResponse({"message": "POST: parameter 'consult_type' not found"}, status=400)
#         consult_type_field = request.POST['consult_type']
#         consulttype = ConsultType(type=consult_type_field)
#         consulttype.save()
#         response = serializers.serialize("json", [consulttype, ])
#         return HttpResponse(response, content_type='application/json')
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except DataError as e:
#         return JsonResponse({"message": str(e)}, status=400)

