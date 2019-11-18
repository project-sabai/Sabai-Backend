from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Visit, PostReferral
from postreferral.forms import PostreferralForm

import json


@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print('data ', data)
        print('gap ,')
        order_form = OrderForm(data)

        if order_form.is_valid():
            # print('this is the consult_form ', consult_form)
            # consult_form.consult_date = request.POST['consult_date']
            # print('doneso ', consult_form )
            order = order_form.save()
            response = serializers.serialize("json", [order, ])
            
            return HttpResponse(response, content_type='application/json')
        else:
            print('failing')
            print(order_form.errors)
            return JsonResponse({"message": order_form.errors}, status=400)
    except ObjectDoesNotExist as e:
        print('this is the error ', e)
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)

# @api_view(['POST'])
# @csrf_exempt
# def create_new(request):
#     try:
#         # if 'visit' not in request.POST:
#         #     return JsonResponse({"message": "POST: parameter 'visit' not found"}, status=400)
#         # visit = request.POST['visit']

#         # Visit.objects.get(pk=visit)
#         postreferral_form = PostreferralForm(request.POST)
#         if postreferral_form.is_valid():
#             postreferral = postreferral_form.save()
#             response = serializers.serialize("json", [postreferral, ])
#             return HttpResponse(response, content_type='application/json')
#         else:
#             return JsonResponse(postreferral_form.errors, status=400)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except DataError as e:
#         return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_details(request):
    try:
        sort_params = request.GET.dict()
        postReferrals = PostReferral.objects.filter(**sort_params)

        response = serializers.serialize('json', postReferrals)

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
        postReferral = PostReferral.objects.filter(**sort_params)

        # updating row and saving changes to DB
        data = json.loads(request.body.decode('utf-8'))
        postReferral.update(**data)

        return JsonResponse({
            "message": "success"
        }, status = 200)

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)