from django.db import models
from datetime import datetime
from login import models as login


class Patient(models.Model):
    class Meta:
        db_table = "patients"

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
    picture_blob = models.BinaryField(blank=True, null=True, editable=True)


class Fingerprint(models.Model):
    class Meta:
        db_table = "fingerprints"

    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fg_value = models.BinaryField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    fg_image = models.BinaryField(blank=True, null=True)


class Visit(models.Model):
    class Meta:
        db_table = "visits"

    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    status = models.CharField(max_length=100)


class Vitals(models.Model):
    class Meta:
        db_table = "vitals"

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    height = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    weight = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    systolic = models.IntegerField(default=0)
    diastolic = models.IntegerField(default=0)
    temperature = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    hiv_positive = models.BooleanField(default=False)
    ptb_positive = models.BooleanField(default=False)
    hepc_positive = models.BooleanField(default=False)
    heart_rate = models.IntegerField(default=0)


class Postreferral(models.Model):
    class Meta:
        db_table = "postreferrals"

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    recorder = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)


class Consult(models.Model):
    class Meta:
        db_table = "consults"

    visit_id = models.ForeignKey(Visit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    doctor = models.ForeignKey(login.User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    urine_test = models.TextField(blank=True, null=True)
    hemocue_count = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    blood_glucose = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    referrals = models.TextField(blank=True, null=True)
    chronic_referral = models.BooleanField(blank=True, null=True)
    addendum = models.TextField(blank=True, null=True)

