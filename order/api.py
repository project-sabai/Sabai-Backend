import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Order
from order.forms import OrderForm

# Remember
# Create
# Read
# Updated
# Delete

@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        order_form = OrderForm(data)

        if order_form.is_valid():
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

@api_view(['POST'])
@csrf_exempt
def migrate(request):
    try:
        data = request.POST.copy()
        order_form = OrderForm(data)

        if order_form.is_valid():
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

@api_view(['GET'])
def get_details(request):
    try:
        sort_params = request.GET.dict()
        orders = Order.objects.filter(**sort_params)

        response = serializers.serialize('json', orders)

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
        order = Order.objects.filter(**sort_params)

        # updating row and saving changes to DB
        data = json.loads(request.body.decode('utf-8'))
        order.update(**data)

        return JsonResponse({
            "message": "success"
        }, status = 200)

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)






# @api_view(['POST'])
# @csrf_exempt
# def create_new(request):
#     try:
#         print(request.POST)
#         form = OrderForm(request.POST)
#         print('form is valid? ', form.is_valid())
#         print(form.errors)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.save()
#             response = serializers.serialize("json", [order])
#             return HttpResponse(response, content_type="application/json")
#         else:
#             return JsonResponse(form.errors, status=400)
#     except DataError as e:
#         return JsonResponse({"message": str(e)}, status=400)

# @api_view(['GET'])
# def get_consults(request):
#     try:
#         sort_params = request.GET.dict()
#         order = Order.objects.filter(**sort_params)
#         response = serializers.serialize('json', order)
#         return HttpResponse(response, content_type="application/json")

#     except Exception as e:
#         return JsonResponse({
#             "message": str(e)
#         }, status = 400)

