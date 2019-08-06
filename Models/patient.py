from django.db import models

class Patient(models.Model):
    id = models.IntegerField
    village_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    travelling_time_to_village = models.IntegerField
    date_of_birth = models.CharField(max_length=10)
    drug_allergy = models.TextField
    parent = models.IntegerField
    face_encodings = models.CharField(max_length=3000)