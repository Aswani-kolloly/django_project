from django import forms
from django.core.validators import RegexValidator

from .models import AgentDetails, CustomUser, MedicalshopDetails, DoctorDetails, PatientDetails, Prescription, Medicine


class RegisterForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            "username": forms.TextInput(attrs={'class': "form-control", 'placeholder': "Username", 'required': True}),
            "password": forms.PasswordInput(
                attrs={'class': "form-control", 'placeholder': "Password", 'required': True}),

        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AgentCreationForm(forms.ModelForm):
    class Meta:
        model = AgentDetails
        fields = ['agency_name', 'address', 'contact_num']
        widgets = {
            "agency_name": forms.TextInput(
                attrs={'class': "form-control", 'placeholder': "Agency name", 'required': True}),
            "address": forms.TextInput(attrs={'class': "form-control", 'placeholder': "Addresse", 'required': True}),
            "contact_num": forms.TextInput(
                attrs={'class': "form-control ", 'placeholder': "Contact no", 'required': True}),
        }


class MedicalshopRegistration(forms.ModelForm):
    class Meta:
        model = MedicalshopDetails
        fields = ['shop_name', 'agent']
        widgets = {
            "shop_name": forms.TextInput(attrs={'class': "form-control",'placeholder': "Shop name", 'required': True}),
            "agent": forms.Select(attrs={'class': "form-control",'readonly': True, 'required': True}),
        }


class DoctorRegistration(forms.ModelForm):
    class Meta:
        model = DoctorDetails
        fields = ['image', 'specialization', 'hospital', 'agent']
        widgets = {
            "specialization": forms.TextInput(attrs={'class': "form-control",'placeholder': "Specialized Area", 'required': True}),
            "image": forms.FileInput(attrs={'class': "form-control",'placeholder': "Photo", 'required': True}),
            "hospital": forms.TextInput(attrs={'class': "form-control",'placeholder': "Hospital", 'required': True}),
            "agent": forms.Select(attrs={'class': "form-control",'readonly': True, 'required': True}),
        }


class PatientRegistration(forms.ModelForm):
    class Meta:
        model = PatientDetails
        fields = ['name', 'gender', 'image', 'dob', 'emergency_contact', 'allergy', 'blood_type', 'agent', 'card_num',
                  'date']
        widgets = {
            "name": forms.TextInput(attrs={'class': "form-control", 'placeholder': "Full name", 'required': True}),
            "image": forms.FileInput(attrs={'class': "form-control", 'placeholder': "Recent photo", 'required': True}),
            "gender": forms.Select(attrs={'class': "form-control", 'placeholder': "Select", 'required': True}),
            "dob": forms.DateInput(
                attrs={'class': "form-control", 'type': 'date', 'placeholder': "Select", 'required': True}),
            "emergency_contact": forms.TextInput(
                attrs={'class': "form-control", 'placeholder': "Contact No.", 'required': True}),
            "allergy": forms.TextInput(
                attrs={'class': "form-control", 'placeholder': "Allergies if any", 'required': True}),
            "blood_type": forms.Select(attrs={'class': "form-control", 'placeholder': "Select ", 'required': True}),
            "card_num": forms.TextInput(
                attrs={'class': "form-control", 'placeholder': "Card No.", 'readonly': True, 'required': True}),
            "date": forms.TextInput(attrs={'class': "form-control", 'readonly': True, 'required': True}),
            "agent": forms.Select(attrs={'class': "form-control",'readonly':True, 'required': True,})
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['prescription', 'name', 'dose', 'quantity']
        widgets = {
            "prescription": forms.TextInput(attrs={'class': "form-control",'readonly':True}),
            "name": forms.TextInput(attrs={'class': "form-control",'required':True}),
            "dose": forms.TextInput(attrs={'class': "form-control",'required':True}),
            "quantity": forms.NumberInput(attrs={'class': "form-control",'required':True}),
        }
