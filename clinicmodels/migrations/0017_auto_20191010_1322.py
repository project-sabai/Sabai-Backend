# Generated by Django 2.2.4 on 2019-10-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0016_auto_20191010_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consult',
            name='consult_date',
            field=models.DateTimeField(),
        ),
    ]