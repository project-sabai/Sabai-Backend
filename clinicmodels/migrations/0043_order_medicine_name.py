# Generated by Django 2.2.4 on 2019-11-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0042_consult_sub_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='medicine_name',
            field=models.CharField(default='loser', max_length=255),
            preserve_default=False,
        ),
    ]