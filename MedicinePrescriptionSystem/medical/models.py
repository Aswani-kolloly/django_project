from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    type_choices = (
        ('Agent', 'agent'),
        ('Doctor', 'doctor'),
        ('Medicalshop', 'medicalshop'),

    )
    user_type = models.CharField(max_length=15,
                                 choices=type_choices)

    def __str__(self):
        return self.username


class AgentDetails(models.Model):
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Invalid phone number.")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    contact_num = models.CharField(validators=[phone_regex],max_length=10)

    def __str__(self):
        return self.user.username


class PatientDetails(models.Model):
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Invalid phone number.")
    gen_choices = (("female", "female"),
                   ("male", "male"))
    blood_types = (("O+", "O+"),
                   ("O-", "O-"),
                   ("A+", "A+"),
                   ("A-", "A"),
                   ("B+", "B+"),
                   ("B-", "B-"),
                   ("AB+", "AB+"),
                   ("AB-", "AB-"))
    image = models.ImageField(upload_to='images/patient/')
    name = models.CharField(max_length=120)
    gender = models.CharField(max_length=10, choices=gen_choices)
    dob = models.DateField()
    date = models.DateField()
    emergency_contact = models.CharField(validators=[phone_regex],max_length=10)
    card_num = models.IntegerField(unique=True)
    allergy = models.CharField(max_length=120)
    blood_type = models.CharField(max_length=20, choices=blood_types)
    agent = models.ForeignKey(AgentDetails, on_delete=models.CASCADE)


class DoctorDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/doctor/')
    specialization = models.CharField(max_length=120)
    hospital = models.CharField(max_length=120)
    agent = models.ForeignKey(AgentDetails, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)



class MedicalshopDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=120)
    agent = models.ForeignKey(AgentDetails, on_delete=models.CASCADE)


class Prescription(models.Model):
    #patient_id = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.SET('Entry deleted'))
    cardnum = models.ForeignKey(PatientDetails, to_field='card_num', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=120)
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

class Medicine(models.Model):
    prescription=models.ForeignKey(Prescription,on_delete=models.CASCADE)
    name=models.CharField(max_length=120)
    quantity=models.IntegerField()
    dose=models.CharField(max_length=120)
    pending=models.IntegerField()
