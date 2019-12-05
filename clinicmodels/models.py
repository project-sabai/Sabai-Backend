from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import JSONField, ArrayField


class Patient(models.Model):
    class Meta:
        db_table = "patients"

    id = models.IntegerField(primary_key=True)
    village_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    local_name = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6)
    travelling_time_to_village = models.IntegerField(default=0)
    date_of_birth = models.DateField(default=timezone.now)
    drug_allergy = models.TextField(default="None")
    parent = models.IntegerField(blank=True, null=True)
    face_encodings = ArrayField(models.FloatField(), blank=True, null=True)
    picture = models.ImageField(upload_to='static/images', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Visit(models.Model):
    class Meta:
        db_table = "visits"

    id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    # date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)
    # medical_consultation = models.BooleanField(default=False)
    # dental_consultation = models.BooleanField(default=False)
    # consultations = JSONField()
    # created_at = models.DateTimeField(auto_now_add=True)
    visit_date=models.DateField(default=timezone.now)
    created_at=models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class MedicalVitals(models.Model):
    class Meta:
        db_table = "medicalVitals"

    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    height = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    weight = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    systolic = models.IntegerField(default=0)
    diastolic = models.IntegerField(default=0)
    temperature = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    hiv_positive = models.BooleanField(default=False)
    ptb_positive = models.BooleanField(default=False)
    hepc_positive = models.BooleanField(default=False)
    heart_rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class DentalVitals(models.Model):
    class Meta:
        db_table = "dentalVitals"
    
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    complaints = models.TextField(blank=True, null=True)
    intraoral = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    
    exo = models.CharField(max_length=255, blank=True, null=True)
    cap = models.CharField(max_length=255, blank=True, null=True)
    sdf = models.CharField(max_length=255, blank=True, null=True)
    f = models.CharField(max_length=255, blank=True, null=True)
    others = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

# For now, we will be leaving doctor & addendum_doctor with a data type as var char
# This is to keep things simple at the moment
# In the future, when a user has more information, then we will transition back to linking to a user
class Consult(models.Model):
    class Meta:
        db_table = "consults"

    id = models.IntegerField(primary_key=True)
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=255)
    sub_type = models.CharField(max_length=255, blank=True, null=True)
    doctor = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    referred_for = models.CharField(max_length=255, blank=True, null=True)
    
    # These are for dental
    exo = models.CharField(max_length=255, blank=True, null=True)
    cap = models.CharField(max_length=255, blank=True, null=True)
    sdf = models.CharField(max_length=255, blank=True, null=True)
    f = models.CharField(max_length=255, blank=True, null=True)
    others = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Addendum(models.Model):
    class Meta:
        db_table = "addendum"

    consult = models.ForeignKey(Consult, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    doctor = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class PostReferral(models.Model):
    class Meta:
        db_table = "postreferrals"

    consult=  models.ForeignKey(Consult, on_delete=models.SET_NULL, blank=True, null=True)
    # date = models.DateTimeField(default=timezone.now)
    doctor = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    # reserve_quantity = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    # remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    class Meta:
        db_table = "order"

    medicine = models.ForeignKey(Medication, on_delete=models.SET_NULL, blank=True, null=True)
    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    doctor = models.CharField(max_length=255)
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    consult = models.ForeignKey(Consult, on_delete= models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class StockTransactions(models.Model):
    class Meta:
        db_table= "stockTransactions"

    medicine = models.ForeignKey(Medication, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.CharField(max_length=255)
    # approve prescription
    # edit stock
    type = models.CharField(max_length=255)
    # can be positive or negative, depending on what kind of transaction happened
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)