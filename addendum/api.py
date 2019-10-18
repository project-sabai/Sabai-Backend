import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Addendum
from addendum.forms import AddendumForm


@api_view(['POST'])
@csrf_exempt
def create_new(request):
    try:
        form = AddendumForm(request.POST)
        if form.is_valid():
            addendum = form.save(commit=False)
            addendum.save()
            response = serializers.serialize("json", [addendum, ])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


# @api_view(['POST'])
# @csrf_exempt
# def update_vitals(request):
#     try:
#         if 'id' not in request.POST:
#             return JsonResponse({"message": "POST: parameter 'id' not found"}, status=400)
#         vitals_id = request.POST['id']
#         vitals = DentalVitals.objects.get(pk=vitals_id)

#         if 'complaints' in request.POST:
#             vitals.complaints = request.POST['complaints']
#         if 'intraoral' in request.POST:
#             vitals.intraoral = request.POST['intraoral']
#         if 'diagnosis' in request.POST:
#             vitals.diagnosis = request.POST['diagnosis']
#         if 'complaints' in request.POST:
#             vitals.others = request.POST['others']
#         if 'complaints' in request.POST:
#             vitals.referred_for = request.POST['referred_for']
            
#         vitals.save()
#         response = serializers.serialize("json", [vitals, ])
#         return HttpResponse(response, content_type='application/json')

#     except DataError as e:
#         return JsonResponse({"message": str(e)}, status=400)
#     except ValueError as e:
#         return JsonResponse({"message": str(e)}, status=400)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message", str(e)}, status=400)
#     except TypeError as e:
#         return JsonResponse({"message", str(e)}, status=400)


# @api_view(['GET'])
# def get_vitals_by_id(request):
#     try:
#         if 'id' not in request.GET:
#             return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
#         vitals_id = request.GET['id']
#         vitals = DentalVitals.objects.get(pk=vitals_id)
#         response = serializers.serialize("json", [vitals, ])
#         return HttpResponse(response, content_type='application/json')
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except ValueError as e:
#         return JsonResponse({"message": str(e)}, status=400)


# @api_view(['GET'])
# def get_vitals_by_visit(request):
#     try:
#         if 'visit_id' not in request.GET:
#             return JsonResponse({"message": "GET: parameter 'visit_id' not found"}, status=400)
#         visit_id = request.GET['visit_id']
#         vitals = DentalVitals.objects.filter(visit=visit_id)
#         response = serializers.serialize("json", vitals)
#         return HttpResponse(response, content_type='application/json')
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except ValueError as e:
#         return JsonResponse({"message": str(e)}, status=400)


# @api_view(['GET'])
# def get_vitals_by_patient(request):
#     try:
#         if 'patient_id' not in request.GET:
#             return JsonResponse({"message": "GET: parameter 'patient_id' not found"}, status=400)
#         patient_id = request.GET['patient_id']
#         vitals = DentalVitals.objects.filter(visit__patient_id=patient_id)
#         response = serializers.serialize("json", vitals)
#         return HttpResponse(response, content_type='application/json')
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except ValueError as e:
#         return JsonResponse({"message": str(e)}, status=400)
