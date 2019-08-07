from clinicmodels.models import Patient
from django.http import JsonResponse


def get_patient_by_name(request):
    patient_name = request.GET['name']
    try:
        patient = Patient.objects.get(name=patient_name)
        print("hi")
        return JsonResponse(patient)
    except:
        return JsonResponse({})

def create_new_patient(request):
    return

