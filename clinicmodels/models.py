from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Patient(models.Model):
    class Meta:
        db_table = "patients"

    village_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    travelling_time_to_village = models.IntegerField(default=0)
    date_of_birth = models.DateField(default=timezone.now)
    drug_allergy = models.TextField(default="None")
    parent = models.IntegerField(blank=True, null=True)
    face_encodings = models.CharField(max_length=3000)
    picture = models.ImageField(upload_to='static/images')


class Fingerprint(models.Model):
    class Meta:
        db_table = "fingerprints"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fg_value = models.BinaryField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    fg_image = models.BinaryField(blank=True, null=True)


class Visit(models.Model):
    class Meta:
        db_table = "visits"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
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
    date = models.DateTimeField(default=timezone.now)
    recorder = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)


class Consult(models.Model):
    class Meta:
        db_table = "consults"

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    urine_test = models.TextField(blank=True, null=True)
    hemocue_count = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    blood_glucose = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    referrals = models.TextField(blank=True, null=True)
    chronic_referral = models.BooleanField(blank=True, null=True)
    addendum = models.TextField(blank=True, null=True)
    addendum_time = models.DateTimeField(blank=True, null=True)


class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class Order(models.Model):
    class Meta:
        db_table = "order"

    medicine = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
