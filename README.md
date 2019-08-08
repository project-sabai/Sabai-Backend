# OpenClinic
A simple to use, self-contained portable clinic application
for use in overseas missions to manage clinic operations.
## API Documentation
The OpenClinic API is separated into different modules.
For example, all functions related to patients is done
by the patients module. The API Documentation will be
separated by these modules.

### Errors
All successful requests return a HTTP status code of 200. 
If the requested resource is not found, a status code of 404
is sent. If the request is malformed due to user error, a status
code of 400 is sent. Any 500 series error indicates a bug on
the application side, and a bugfix request will need to be sent.

### Patient
#### GET: /patients/by_name
Parameters:
```
name: Full or partial name of the patient(s) you want 
to retrieve
```
This endpoint retrieves an array of patient objects. The
'name' parameter is used as a substring to retrieve all
patients with that string in their name.

Result:
```
[
  {
    "model": "clinicmodels.patient",
    "pk": 1,
    "fields": {
      "village_prefix": "TGV",
      "name": "Aloha Samsam",
      "contact_no": "12345678",
      "gender": "Female",
      "travelling_time_to_village": 30,
      "date_of_birth": "1995-09-30",
      "drug_allergy": "all",
      "parent": 1,
      "face_encodings": "22",
      "picture": "static/images/Screenshot_1_w0Aipr6.png"
    }
  }
]
```

#### GET: /patients/by_id
Parameters:
```
id: Primary key of the Patient you want to retrieve
```
This endpoint retrieves a Patient object in a one element 
array according to the primary key provided by the id.