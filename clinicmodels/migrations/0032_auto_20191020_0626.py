# Generated by Django 2.2.4 on 2019-10-20 06:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0031_order_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='drug_allergy',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='patient',
            name='face_encodings',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
