# Generated by Django 3.1.7 on 2021-06-01 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0002_auto_20210601_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctordetails',
            old_name='type',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='medicalshopdetails',
            old_name='type',
            new_name='user',
        ),
    ]
