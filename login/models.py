from django.db import models

class User(models.Model):
    class Meta:
        db_table = "users"
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)