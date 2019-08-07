from clinicmodels.models import Patient
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.core import serializers

from patient.forms import PatientForm


def get_patient_by_name(request):
    patient_name = request.GET['name']

    try:
        patient = Patient.objects.get(name=patient_name)
        return JsonResponse(list(patient.values))
    except MultiValueDictKeyError:
        return JsonResponse({})


def get_patient_by_id(request):
    patient_id = request.GET['id']

    try:
        patient = Patient.objects.filter(id=patient_id)
        response = serializers.serialize("json", patient)
        return HttpResponse(response, content_type='application/json')
    except MultiValueDictKeyError:
        return JsonResponse({})


@csrf_exempt
def create_new_patient(request):
    form = PatientForm(request.POST, auto_id=True)
    if form.is_valid():
        print("great!")
        print(form)
        patient = form.save(commit=False)
        patient.save()
    else:
        print("crap")
    return JsonResponse({})
