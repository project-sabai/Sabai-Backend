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
        print(request.POST)
        form = OrderForm(request.POST)
        print('form is valid? ', form.is_valid())
        print(form.errors)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            response = serializers.serialize("json", [order])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def get_consults(request):
    try:
        sort_params = request.GET.dict()
        order = Order.objects.filter(**sort_params)
        response = serializers.serialize('json', order)
        return HttpResponse(response, content_type="application/json")

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)

