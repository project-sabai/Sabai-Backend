from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Visit
from postreferral.forms import PostreferralForm


@api_view(['POST'])
@csrf_exempt
def create_new_postreferral(request):
    try:
        if 'visit' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'visit' not found"}, status=400)
        visit = request.POST['visit']

        Visit.objects.get(pk=visit)
        postreferral_form = PostreferralForm(request.POST)
        if postreferral_form.is_valid():
            postreferral = postreferral_form.save()
            response = serializers.serialize("json", [postreferral, ])
            return HttpResponse(response, content_type='application/json')
        else:
            return JsonResponse(postreferral_form.errors, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)
