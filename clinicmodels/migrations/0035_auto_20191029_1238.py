# Generated by Django 2.2.4 on 2019-10-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0034_auto_20191028_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='drug_allergy',
            field=models.TextField(default='None'),
        ),
    ]