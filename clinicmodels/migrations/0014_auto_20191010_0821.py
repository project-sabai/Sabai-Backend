# Generated by Django 2.2.4 on 2019-10-10 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0013_consult_blood_glucose_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consult',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
