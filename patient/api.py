from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from clinicmodels.models import Patient
from patient.forms import PatientForm
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

import json
import base64
import uuid
import face_recognition
import copy

"""
Handles all operations regarding the retrieval, update of patient models.
"""

# THIS IS THE MODEL EXAMPLE!!!!
@api_view(['GET'])
def get_details(request):
    try:
        sort_params = request.GET.dict()
        patients = Patient.objects.filter(**sort_params)

        # create a copy of the QueryDict
        
        # get image file
        # convert to base64
        # set base64 as new value of picture
        
        print('this is patients ', patients.values())
        response = serializers.serialize('json', patients)

        

        return HttpResponse(response, content_type="application/json")
    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)

@api_view(['POST'])
def find_by_scan(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        image_data = data['imageDetails']

        header, base64Data = image_data.split(';base64,')   

        try:
            decoded_file = base64.b64decode(base64Data)
        except TypeError:
            print('invalid image')
        
        image_file = ContentFile(decoded_file, name='temp.jpeg')

        known_image = face_recognition.load_image_file(image_file)
        encoding = face_recognition.face_encodings(known_image)[0]

        sort_params = request.GET.dict()
        patients = Patient.objects.filter(**sort_params)
        patients_list = list(patients.values())

        encode_list = []
        potential_pk_list = []

        for patient in patients_list:
            try:
                other_encoding = patient['face_encodings']

                if len(other_encoding) > 0:
                    encode_list.append(other_encoding)
                    potential_pk_list.append(patient['id'])
            except Exception as e:
                print('error')



        match_pk_list = []
        results = face_recognition.compare_faces(encode_list, encoding, 0.5)
        count = 0
        index = 0

        print('len results ', results)
        while count < 5 and index < len(results):
            print('this one ...', index)
            if results[index]:
                count += 1
                match_pk_list.append(potential_pk_list[index])
            index += 1

        filteredPatients = Patient.objects.filter(pk__in=match_pk_list)
        response = serializers.serialize('json', filteredPatients)

        return HttpResponse(response, content_type="application/json")
    except Exception as e:
        print('this is the error ', e)
        
        return JsonResponse({
            "message": str(e)
        }, status = 400)

    
    
    
    # receives an image
    # convert to file format
    # get all images from db

    # do face recognition

    # receive array of 

@api_view(['PATCH'])
def update_details(request):
    try:
        # finding row to update
        sort_params = request.query_params.dict()
        patient = Patient.objects.filter(**sort_params)

        # updating row and saving changes to DB
        data = json.loads(request.body.decode('utf-8'))
        patient.update(**data)

        return JsonResponse({
            "message": "success"
        }, status = 200)

    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status = 400)

@api_view(['POST'])
@csrf_exempt
def create_new(request):
    '''
    POST request with multipart form to create a new patient
    :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
    :return: Http Response with corresponding status code
    '''
    
    
    try:
        # print('look here fam ', request.POST['id'])
        print('post ', request)
        print('post data ', json.loads(request.body.decode('utf-8')))
        print('post files ', request.FILES)

        data = json.loads(request.body.decode('utf-8'))
        image_data  = data['imageDetails']
        # print('image data ', image_data)

        header, base64Data = image_data.split(';base64,')

        try:
            decoded_file =  base64.b64decode(base64Data)
        except TypeError:
            print('invalid image')
        
        file_name = str(uuid.uuid4())[:12]
        complete_file_name = '{}.jpeg'.format(file_name)

        request.FILES['picture'] = ContentFile(decoded_file, name=complete_file_name)
        image = ContentFile(decoded_file, name='temp.jpeg')

        known_image = face_recognition.load_image_file(image)
        encoding = face_recognition.face_encodings(known_image)
        if len(encoding) == 0:
            return JsonResponse({"error": "Face not found"}, status=200)

        encoding_enriched = []
        for num in encoding[0]:
            encoding_enriched.append(num.item())
        
        data['face_encodings'] = encoding_enriched
        print('final product ', request.FILES)

        form  = PatientForm(data, request.FILES)
        print()
        print('=====')
        print('form here ', form)
        print('=====')
        # form = PatientForm(request.POST, request.FILES)
        # print('this is form homie ', form)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            response = serializers.serialize("json", [patient, ])
            return HttpResponse(response, content_type="application/json")
        else:
            print('look here ', form.errors)
            return JsonResponse(form.errors, status=400)
        return JsonResponse({}, status=500)
    except DataError as e:
        print()
        print('and this is your error ', e)
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['POST'])
@csrf_exempt
def migrate(request):
    '''
    POST request with multipart form to create a new patient
    :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
    :return: Http Response with corresponding status code
    '''
    
    
    try:
        print('look here fam ', request.POST['id'])
        print('post ', request)
        # print('post data ', json.loads(request.body.decode('utf-8')))
        print('post files ', request.FILES)

        data = request.POST.copy()
        image = copy.deepcopy(request.FILES['picture'])

        known_image = face_recognition.load_image_file(image)
        encoding = face_recognition.face_encodings(known_image)
        # if len(encoding) == 0:
        #     return JsonResponse({"error": "Face not found"}, status=200)

        encoding_enriched = []
        if len(encoding) > 0:
            for num in encoding[0]:
                encoding_enriched.append(num.item())
        
        data['face_encodings'] = encoding_enriched

        form  = PatientForm(data, request.FILES)
        print()
        print('=====')
        print('form here ', form)
        print('=====')
        # form = PatientForm(request.POST, request.FILES)
        # print('this is form homie ', form)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            response = serializers.serialize("json", [patient, ])
            return HttpResponse(response, content_type="application/json")
        else:
            print('look here ', form.errors)
            return JsonResponse(form.errors, status=400)
        return JsonResponse({}, status=500)
    except DataError as e:
        print()
        print('and this is your error ', e)
        return JsonResponse({"message": str(e)}, status=400)



