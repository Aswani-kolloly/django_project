# Generated by Django 3.1.7 on 2021-06-01 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0003_auto_20210601_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetails',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
