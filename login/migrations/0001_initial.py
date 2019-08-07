# Generated by Django 2.2.4 on 2019-08-07 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('account_type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
