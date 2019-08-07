from django.db import models
from datetime import datetime

class Patient(models.Model):
    class Meta:
        db_table = "patient"
    id = models.IntegerField(primary_key=True)
    village_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    travelling_time_to_village = models.IntegerField(default=0)
    date_of_birth = models.CharField(max_length=10)
    drug_allergy = models.TextField(default="None")
    parent = models.IntegerField(blank=True, null=True)
    face_encodings = models.CharField(max_length=3000)

class Visits(models.Model):
    class Meta:
        db_table = "visits"
    id = models.IntegerField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    status = models.CharField(max_length=100)

class Vitals(models.Model):
    class Meta:
        db_table = "vitals"
    vitals_id = models.IntegerField(primary_key=True, default=0)
    visit = models.ForeignKey(Visits, on_delete=models.CASCADE)
    height = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    weight = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    systolic = models.IntegerField(default=0)
    diastolic = models.IntegerField(default=0)
    temperature = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    hiv_positive = models.BooleanField(default=False)
    ptb_positive = models.BooleanField(default=False)
    hepc_positive = models.BooleanField(default=False)
    heart_rate = models.IntegerField(default=0)