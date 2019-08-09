from django.core import serializers
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from vitals.forms import VitalsForm


@api_view(['POST'])
@csrf_exempt
def create_new_vitals(request):
    try:
        form = VitalsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.save()
            response = serializers.serialize("json", [vitals, ])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)
