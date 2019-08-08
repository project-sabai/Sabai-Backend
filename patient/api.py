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
    except MultiValueDictKeyError:
        return JsonResponse({})


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
    except MultiValueDictKeyError:
        raise Http404("Patient not found")
    except IndexError:
        raise Http404("Patient not found")


def get_patient_image_by_id(request):
    patient_id = request.GET['id']
    try:
        patient = Patient.objects.filter(id=patient_id)[0]
        binary = patient.picture_blob.file
        binary_io = io.BytesIO(binary.read())
        response = FileResponse(binary_io)
        response['Content-Type'] = 'application/x-binary'
        binary.close()
        return response
    except MultiValueDictKeyError as e:
        raise Http404("Patient image does not exist")
    except IndexError as e:
        raise Http404("Patient image does not exist")


@csrf_exempt
def create_new_patient(request):
    '''
    POST request with multipart form to create a new patient
    :param request: POST request with the required parameters
    :return: Http Response with corresponding status code
    '''
    form = PatientForm(request.POST, request.FILES)
    print(form)
    if form.is_valid():
        print("great!")
        print(form)
        patient = form.save(commit=False)
        patient.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
