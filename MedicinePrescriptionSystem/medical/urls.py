"""MedicinePrescriptionSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("", LandingPage.as_view(), name="landingpage"),
    path("doctors-dashboard/", DoctorsDashboard.as_view(), name="doctors-dashboard"),
    path("agent-dashboard/", AgentDashboard.as_view(), name="agent-dashboard"),
    path("agent-registration/", AgentCreation.as_view(), name="agent-registration"),
    path("patient-registration/", PatientsAccountCreation.as_view(), name="patient-registration"),
    path("doctor-registration/", DoctorsAccountCreation.as_view(), name="doctors-registration"),
    path("medicalshop-dashboard/", MedicalshopDashboard.as_view(), name="medicalshop-dashboard"),
    path("medicalshop-registration/",MedicalshopCreation.as_view(),name="medicalshop-registration"),
    path("med-history/<int:cardnum>", MedicalHistory.as_view(), name="med-history"),
    path("view-medicine/<int:pres_id>", ViewMedicine.as_view(), name="view-med"),
    path("pending-medicine/<int:pres_id>/<int:cardnum>",PendingMedicines.as_view(),name="pending-med"),
    path("add-prescription/<int:cardnum>", AddPrescription.as_view(), name="add-prescription"),
    path("add-medicine/<int:pres_id>/<int:cardnum>", AddMedicine.as_view(), name="add-medicine"),
    path("old-prescriptions/<int:cardnum>",ViewOldPrescriptions.as_view(),name="old-prescriptions"),
    path("pending-prescriptions/<int:cardnum>",PendingPrescriptions.as_view(),name="pending-prescriptions"),
    path("error-page/", error_page, name="error-page"),
    path("logout/", user_logout, name="logout"),
    path("editMed/<int:pres_id>/<int:med_id>/<int:cardnum>",EditMedicine.as_view(),name="editMed"),
    path("view-old-med/<int:pres_id>/<int:cardnum>",ViewOldMed.as_view(),name="view-old-med"),
    path("edit-old-med/<int:pres_id>/<int:med_id>/<int:cardnum>",EditOldMed.as_view(),name="edit-old-med")




]
