from clinicmodels.models import Patient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.forms.models import model_to_dict

from patient.forms import PatientForm


def get_patient_by_name(request):
    patient_name = request.GET['name']

    try:
        patient = Patient.objects.get(name=patient_name)
        return JsonResponse({"id" : patient.id})
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
