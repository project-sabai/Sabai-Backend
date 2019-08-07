from clinicmodels.models import Patient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from patient.forms import NewPatientForm


def get_patient_by_name(request):
    patient_name = request.GET['name']
    try:
        patient = Patient.objects.get(name=patient_name)
        print("hi")
        return JsonResponse(patient)
    except:
        return JsonResponse({})

@csrf_exempt
def create_new_patient(request):
    form = NewPatientForm(request.POST)
    if form.is_valid():
        print("great!")
    else:
        print("crap")
    return JsonResponse({})
