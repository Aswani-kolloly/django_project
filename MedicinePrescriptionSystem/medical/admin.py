from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AgentDetails,PatientDetails,DoctorDetails,MedicalshopDetails,CustomUser

# Register your models here.
admin.site.register(CustomUser,UserAdmin)
admin.site.register(AgentDetails)
admin.site.register(PatientDetails)
admin.site.register(DoctorDetails)
admin.site.register(MedicalshopDetails)
