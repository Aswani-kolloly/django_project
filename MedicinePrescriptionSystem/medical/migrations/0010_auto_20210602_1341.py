# Generated by Django 3.1.7 on 2021-06-02 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0009_auto_20210602_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='blood_type',
            field=models.CharField(choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=20),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='card_num',
            field=models.IntegerField(unique=True),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(max_length=120)),
                ('date', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('cardnum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.patientdetails', to_field='card_num')),
                ('doc_id', models.ForeignKey(on_delete=models.SET('Entry deleted'), to='medical.doctordetails')),
            ],
        ),
        migrations.CreateModel(
            name='Medicice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('qty', models.IntegerField()),
                ('dose', models.CharField(max_length=120)),
                ('pending', models.CharField(default='True', max_length=15)),
                ('pres_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.prescription')),
            ],
        ),
    ]
