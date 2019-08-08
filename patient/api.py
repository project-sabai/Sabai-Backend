import io

from clinicmodels.models import Patient
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.core import serializers

from patient.forms import PatientForm


def get_patient_by_name(request):
    """
    GET patient by name
    :param request: GET request with a name parameter
    :return: JSON Response with an array of users matching name
    """
    patient_name = request.GET['name']

    try:
        patient = Patient.objects.get(name=patient_name)
        return JsonResponse(list(patient.values))
    except (MultiValueDictKeyError, IndexError):
        return JsonResponse({"message": "Patient not found"}, status=404)


def get_patient_by_id(request):
    '''
    GET patient identified by id
    :param request: GET request with an id parameter
    :return: JSON Response with an array of users mathing id
    '''
    patient_id = request.GET['id']

    try:
        patient = Patient.objects.filter(id=patient_id)
        response = serializers.serialize("json", patient)
        return HttpResponse(response, content_type='application/json')
    except (MultiValueDictKeyError, IndexError):
        return JsonResponse({"message": "Patient not found"}, status=404)


def get_patient_image_by_id(request):
    '''
    GET image of patient by id
    :param request: GET with parameter id of patient you want the image of
    :return: FileResponse if image is found, 404 if not
    '''
    patient_id = request.GET['id']
    try:
        patient = Patient.objects.filter(id=patient_id)[0]
        image = patient.picture
        if "jpeg" in image.name.lower():
            return HttpResponse(image.file.read(), content_type="image/jpeg")
        elif "png" in image.name.lower():
            return HttpResponse(image.file.read(), content_type="image/png")
        else:
            return JsonResponse({"message": "Patient image is in the wrong format"}, status=400)
    except (MultiValueDictKeyError, IndexError) as e:
        return JsonResponse({"message": "Patient image does not exist"}, status=404)


@csrf_exempt
def create_new_patient(request):
    '''
    POST request with multipart form to create a new patient
    :param request: POST request with the required parameters
    :return: Http Response with corresponding status code
    '''
    form = PatientForm(request.POST, request.FILES)
    if form.is_valid():
        patient = form.save(commit=False)
        patient.save()
        response = serializers.serialize("json", [patient, ])
        return HttpResponse(response, content_type="application/json")
    else:
        return JsonResponse({"message": "Malformed form, please check your fields"}, status=400)
