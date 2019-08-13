# Generated by Django 2.2.4 on 2019-08-13 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0005_auto_20190813_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='consult',
        ),
        migrations.AddField(
            model_name='order',
            name='visit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinicmodels.Visit'),
        ),
    ]
