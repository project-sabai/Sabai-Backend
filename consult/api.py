from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import ConsultType


@api_view(['GET'])
def get_all_consult_types(request):
    try:
        consulttypes = ConsultType.objects.all()
        if consulttypes.count() == 0:
            return JsonResponse({"message": "ConsultType matching query does not exist"}, status=404)
        response = serializers.serialize("json", consulttypes)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
def create_new_consult_type(request):
    try:
        if 'consult_type' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'consult_type' not found"}, status=400)
        consult_type_field = request.POST['consult_type']
        consulttype = ConsultType(type=consult_type_field)
        consulttype.save()
        response = serializers.serialize("json", [consulttype, ])
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
@csrf_exempt
def create_new_consult(request):
    if 'visit' not in request.POST:
        return JsonResponse({"message": "POST: parameter 'visit' not found"}, status=400)
    return JsonResponse({})
