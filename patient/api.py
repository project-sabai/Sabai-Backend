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
        face_locations = face_recognition.face_locations(known_image)
        print(face_locations)
        # print(known_image)
        encoding = face_recognition.face_encodings(known_image)[0]
        print('this is ', encoding)

        patients = Patient.objects.all()
        patients_list = list(patients.values())

        encode_list = []
        who_list = []

        for patient in patients_list:
            try:
                image = patient['picture']
                name = patient['name']
                other_image = face_recognition.load_image_file('{}'.format(image))
                
                other_encoding = face_recognition.face_encodings(other_image)
                if len(other_encoding) > 0:
                    # print(other_encoding[0])
                    # print('')
                    encode_list.append(other_encoding[0])
                    who_list.append(name)
            except Exception as e:
                print('error')

        print('weeeee')
        # print(list(patients.values())[-1])
        # print('???')

        # patient = list(patients.values())[-5]
        # image_1 = patient['picture']

        # other_image = face_recognition.load_image_file('{}'.format(image_1))
        # other_encoding = face_recognition.face_encodings(other_image)[0]

        # print(other_encoding)

        results = face_recognition.compare_faces(encode_list, encoding, 0.5)
        count = 0
        for i in range(len(results)):
            if results[i]:
                count += 1
                print('this is the guy ', who_list[i])
        print('num matched ', count)

        # try:
        #     img = open("../Sabai-Backend/{0}".format(image),'r+b')
        #     # img = open("../final2018/kek.jpeg", 'rb')
        #     print('photo success')
        # except IOError:
        #     img = None
        #     print("Error in opening image")

        return JsonResponse({
            "message": 'success'
        }, status = 400)
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
        print('this is the final product ', request.FILES)


        form  = PatientForm(data, request.FILES)
        # form = PatientForm(request.POST, request.FILES)
        print('this is form homie ', form)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            response = serializers.serialize("json", [patient, ])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
        return JsonResponse({}, status=500)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)



