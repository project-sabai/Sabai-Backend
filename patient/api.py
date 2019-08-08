from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from clinicmodels.models import Patient
from patient.forms import PatientForm

"""
Handles all operations regarding the retrieval, update of patient models.
"""


def get_patient_by_name(request):
    """
    GET patient by name
    :param request: GET request with a name parameter
    :return: JSON Response with an array of users matching name
    """
    try:
        patient_name = request.GET['name']
        patient = Patient.objects.filter(name__contains=patient_name)
        response = serializers.serialize("json", patient)
        return HttpResponse(response, content_type='application/json')
    except MultiValueDictKeyError:
        return JsonResponse({"message": "GET: parameter 'name' not found"}, status=404)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)


def get_patient_by_id(request):
    '''
    GET patient identified by id
    :param request: GET request with an id parameter
    :return: JSON Response with an array of users mathing id
    '''

    try:
        patient_id = request.GET['id']
        patient = Patient.objects.filter(id=patient_id)
        response = serializers.serialize("json", patient)
        return HttpResponse(response, content_type='application/json')
    except MultiValueDictKeyError:
        return JsonResponse({"message": "GET: parameter 'id' not found"}, status=404)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)


def get_patient_image_by_id(request):
    '''
    GET image of patient by id
    :param request: GET with parameter id of patient you want the image of
    :return: FileResponse if image is found, 404 if not
    '''
    try:
        patient_id = request.GET['id']
        patient = Patient.objects.get(pk=patient_id)
        image = patient.picture
        if "jpeg" in image.name.lower():
            return HttpResponse(image.file.read(), content_type="image/jpeg")
        elif "png" in image.name.lower():
            return HttpResponse(image.file.read(), content_type="image/png")
        else:
            return JsonResponse({"message": "Patient image is in the wrong format"}, status=400)
    except MultiValueDictKeyError:
        return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)


@csrf_exempt
def create_new_patient(request):
    '''
    POST request with multipart form to create a new patient
    :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
    :return: Http Response with corresponding status code
    '''
    form = PatientForm(request.POST, request.FILES)
    if form.is_valid():
        patient = form.save(commit=False)
        patient.save()
        response = serializers.serialize("json", [patient, ])
        return HttpResponse(response, content_type="application/json")
    else:
        return JsonResponse(form.errors, status=400)


@csrf_exempt
def update_patient(request):
    '''
    Update patient data based on the parameters
    :param request: POST with data
    :return: JSON Response with new data, or error
    '''
    try:
        patient_id = request.POST['id']
        try:
            patient = Patient.objects.get(pk=patient_id)
            form = PatientForm(request.POST, request.FILES, instance=patient)
            if form.is_valid():
                edited = form.save()
                response = serializers.serialize("json", [edited, ])
                return HttpResponse(response, content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)

    except MultiValueDictKeyError as e:
        return JsonResponse({"message": "Could not find parameter: id"}, status=400)
