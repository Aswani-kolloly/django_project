# Generated by Django 3.1.7 on 2021-06-02 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0005_auto_20210602_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetails',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
