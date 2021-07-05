from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Exists, Q, OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

# Create your views here.
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import PatientDetails, Prescription, DoctorDetails, Medicine, AgentDetails
from medical.forms import RegisterForm, AgentCreationForm, DoctorRegistration, MedicalshopRegistration, \
    PatientRegistration, MedicineForm
from medical.models import CustomUser


def admin_permission_required(func):
    def wrapper(req, **kwargs):
        if not req.user.is_superuser:
            return redirect("error-page")
        else:
            return func(req, **kwargs)

    return wrapper


def agent_permission_required(func):
    def wrapper(req, **kwargs):
        print(req.user.user_type)
        if req.user.user_type != "Agent":
            return redirect("error-page")
        else:
            return func(req, **kwargs)

    return wrapper


def error_page(req):
    return render(req, "medical/error-page.html")


# login nd landing page here
class LandingPage(TemplateView):
    template_name = "medical/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, req, *args, **kwargs):
        uname = req.POST.get("username")
        pswd = req.POST.get("pass")
        user = authenticate(req, username=uname, password=pswd)
        print(user)
        # print(user.user_type)
        if user:
            print("login success")
            login(req, user)
            if user.user_type == "Agent":
                return redirect("agent-dashboard")
            elif user.user_type == "Doctor":
                return redirect("doctors-dashboard")
            elif user.user_type == "Medicalshop":
                return redirect("medicalshop-dashboard")
            elif user.is_superuser:
                return redirect("agent-registration")
            else:
                return redirect("error-page")
        else:
            print("failed")
            messages.error(req, message="Invalid username or password")
            print(self.request.path_info)
        return HttpResponseRedirect(self.request.path_info)


# medicalshop's actions
class MedicalshopDashboard(TemplateView):
    template_name = "medical/medicalshop-dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        cardno = request.POST.get("cardnum")
        if request.POST.get("viewpres"):
            return redirect("pending-prescriptions", cardnum=cardno)


class PendingMedicines(TemplateView):
    template_name = "medical/pending-medicine.html"
    context = {}

    def get(self, request, *args, **kwargs):
        pres_id = kwargs.get("pres_id")
        cardnum=kwargs.get("cardnum")
        self.context["cardnum"]=cardnum
        pres_obj = Prescription.objects.get(id=pres_id)
        print(pres_id)
        med_list = Medicine.objects.filter(prescription_id=pres_obj, pending__gt=0)
        if not med_list:
            self.context["message"] = "No pending Medicines"
            self.context["presid"] = pres_id
        self.context["med_list"] = med_list
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        qty = request.POST.get("qty")
        print("post", qty)
        pres_id = kwargs.get("pres_id")
        cardnum=kwargs.get("cardnum")
        med_id = request.POST.get("med_id")
        print(med_id)
        med_obj = Medicine.objects.get(id=med_id)
        print(med_obj)
        med_obj.pending = med_obj.pending - int(qty)
        med_obj.save()
        return redirect("pending-med", pres_id=pres_id,cardnum=cardnum)


class PendingPrescriptions(TemplateView):
    template_name = "medical/pending-prescriptions.html"
    context = context = {}

    def get(self, request, *args, **kwargs):
        cardno = kwargs.get("cardnum")
        self.context["cardnum"]=cardno
        print(cardno)
        print(request.user.id)
        pres_obj_list = Prescription.objects.filter(
            ~Exists(
                Medicine.objects.filter(~Q(pending=0), prescription_id=OuterRef('pk'))
            ),
            status=0,cardnum=cardno
        )

        for obj in pres_obj_list:
            obj.status = 1
            obj.save()
        pres_obj = Prescription.objects.filter(cardnum=cardno, status=0)
        print(pres_obj)
        if not pres_obj:
            self.context["message"] = "No pending Prescriptions"
            print("none")
        else:
            print("not empty")
            self.context["pres_obj"] = pres_obj
        return render(request, self.template_name, self.context)


# Doctor's actions
class ViewOldPrescriptions(TemplateView):
    template_name = "medical/old-prescriptions.html"
    context = {}

    def get(self, request, *args, **kwargs):
        cardno = kwargs.get("cardnum")
        self.context["cardnum"]=cardno
        print(cardno)
        print(request.user.id)
        doc_obj = DoctorDetails.objects.get(user=request.user.id)
        pres_obj = Prescription.objects.filter(cardnum_id=cardno, doctor=doc_obj)
        print(pres_obj)
        if not pres_obj:
            self.context["message"] = "No entries yet"
            print("none")
        else:
            print("not empty")
            self.context["pres_obj"] = pres_obj
        return render(request, self.template_name, self.context)

class ViewOldMed(TemplateView):
    template_name = "medical/view-old-med.html"
    context = {}
    def get(self, request, *args, **kwargs):
        pres_id=kwargs.get("pres_id")
        cardnum=kwargs.get("cardnum")
        self.context["cardnum"]=cardnum
        pres_obj = Prescription.objects.get(id=pres_id)
        print(pres_id)
        med_list = Medicine.objects.filter(prescription_id=pres_obj)
        self.context["med_list"] = med_list
        self.context["pres_id"]=pres_id
        return render(request, self.template_name, self.context)


class MedicalHistory(TemplateView):
    template_name = "medical/med-history.html"
    context = {}

    def get(self, request, *args, **kwargs):
        cardno = kwargs.get("cardnum")
        print(cardno)
        pres_obj = Prescription.objects.filter(cardnum_id=cardno)
        print(pres_obj)
        if not pres_obj:
            self.context["message"] = "No entries yet"
            print("none")
        else:
            print("not empty")
            self.context["pres_obj"] = pres_obj
        return render(request, self.template_name, self.context)


class ViewMedicine(TemplateView):
    template_name = "medical/view-medicine.html"
    context = {}

    def get(self, request, *args, **kwargs):
        pres_id = kwargs.get("pres_id")
        pres_obj = Prescription.objects.get(id=pres_id)
        print(pres_id)
        med_list = Medicine.objects.filter(prescription_id=pres_obj)
        self.context["med_list"] = med_list
        return render(request, self.template_name, self.context)


class AddPrescription(TemplateView):
    template_name = "medical/add-prescription.html"
    model = Prescription
    context = {}

    def get(self, request, *args, **kwargs):
        cardnum = kwargs.get("cardnum")
        obj = PatientDetails.objects.get(card_num=cardnum)
        self.context["patient_details"] = obj
        self.context["cardnum"] = cardnum
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        remarks = request.POST.get("remarks")
        cardnum = kwargs.get("cardnum")
        cno = PatientDetails.objects.get(card_num=cardnum)
        usr_obj = CustomUser.objects.get(username=request.user)
        doc_obj = DoctorDetails.objects.get(user=usr_obj.id)
        object = self.model(doctor=doc_obj, cardnum=cno, remarks=remarks)
        object.save()
        print("saved")
        obj = Prescription.objects.filter(cardnum=cardnum).last()
        return redirect("add-medicine", pres_id=obj.id,cardnum=cardnum)
class EditOldMed(TemplateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "medical/edit-med2.html"
    context = {}
    def get_object(self,pid,mid):
        p_obj=Prescription.objects.get(id=pid)
        return self.model.objects.get(id=mid,prescription=p_obj)

    def get(self, request, *args, **kwargs):
        pid = kwargs["pres_id"]
        mid = kwargs["med_id"]

        obj = self.get_object(pid,mid)
        form_obj = self.form_class(instance=obj)
        self.context["form"] = form_obj
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        pid=kwargs.get("pres_id")
        mid=kwargs.get("med_id")
        cardnum = kwargs.get("cardnum")
        #next=request.GET.get('next','')
        obj = self.get_object(pid, mid)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            med = request.POST.get("name")
            dose = request.POST.get("dose")
            qty = request.POST.get("quantity")
            obj.name = med
            obj.quantity = qty
            obj.dose = dose
            obj.pending = qty
            obj.save()
            return redirect("view-old-med",pid,cardnum)

        else:
            messages.error(request,message="Invalid form data")
            self.context["form"] = form
            return render(request, self.template_name, self.context)

class EditMedicine(TemplateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "medical/med-edit.html"
    context = {}
    def get_object(self,pid,mid):
        p_obj=Prescription.objects.get(id=pid)
        return self.model.objects.get(id=mid,prescription=p_obj)

    def get(self, request, *args, **kwargs):
        pid = kwargs["pres_id"]
        mid = kwargs["med_id"]
        obj = self.get_object(pid,mid)
        form_obj = self.form_class(instance=obj)
        self.context["form"] = form_obj
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        pid=kwargs.get("pres_id")
        mid=kwargs.get("med_id")
        cardnum=kwargs.get("cardnum")
        #next=request.GET.get('next','')
        print(next)
        obj = self.get_object(pid, mid)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            med = request.POST.get("name")
            dose = request.POST.get("dose")
            qty = request.POST.get("quantity")
            print()
            obj.name=med
            obj.quantity=qty
            obj.dose=dose
            obj.pending=qty
            obj.save()
            return redirect("add-medicine",pres_id=pid,cardnum=cardnum)
        else:
            messages.error(request,message="Invalid form data")
            self.context["form"] = form
            return render(request, self.template_name, self.context)

class AddMedicine(TemplateView):
    template_name = "medical/add-medicine.html"
    form_class = MedicineForm
    model = Medicine
    context = {}

    def get(self, request, *args, **kwargs):
        pres_id = kwargs.get("pres_id")
        pres_obj = Prescription.objects.get(id=pres_id)
        cardnum = kwargs.get("cardnum")
        self.context["cardnum"]=cardnum
        med_form = self.form_class()
        self.context["med_form"] = med_form
        self.context["pres_id"] = pres_id
        print(pres_id)
        med_list = self.model.objects.filter(prescription_id=pres_obj)
        self.context["med_list"] = med_list
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pres_id = kwargs.get("pres_id")
        pres_obj = Prescription.objects.get(id=pres_id)
        cardnum = kwargs.get("cardnum")
        med = request.POST.get("medicine")
        print(med)
        dose = request.POST.get("dose")
        qty = request.POST.get("qty")
        med_obj = self.model(prescription=pres_obj, name=med, quantity=qty, dose=dose,pending=qty)
        med_obj.save()
        #messages.success(request,message="Added")
        return redirect("add-medicine", pres_id=pres_id,cardnum=cardnum)


# Follows all dashboard redirecting
class DoctorsDashboard(TemplateView):
    template_name = "medical/doctors-dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        cardno = request.POST.get("cardnum")

        if 'addpres' in request.POST:
            return redirect("add-prescription", cardnum=cardno)
        if 'viewhistory' in request.POST:
            return redirect("med-history", cardnum=cardno)
        if 'viewpres' in request.POST:
            return redirect("old-prescriptions", cardnum=cardno)


class AgentDashboard(TemplateView):
    template_name = "medical/agent-dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Follows All profile creations
@method_decorator(admin_permission_required, name='dispatch')
class AgentCreation(TemplateView):
    template_name = "medical/agent-reg.html"
    context = {}

    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        agent_form = AgentCreationForm()
        self.context["register_form"] = register_form
        self.context["agent_form"] = agent_form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user_reg = RegisterForm(request.POST)
        agent_det = AgentCreationForm(request.POST)
        if user_reg.is_valid() and agent_det.is_valid():
            print("valid")
            user = user_reg.save()
            user.user_type = "Agent"
            user.save()
            agent = agent_det.save(commit=False)
            agent.user = user
            agent.save()
            messages.success(request, message="Registration successful")
            return redirect("agent-registration")
        else:
            print(user_reg.errors)
            print(agent_det.errors)
            messages.error(request, message="Invalid form data")
            self.context["register_form"] = user_reg
            self.context["agent_form"] = agent_det
            return render(request, self.template_name, self.context)


@method_decorator(agent_permission_required, name='dispatch')
class MedicalshopCreation(TemplateView):
    template_name = "medical/med-shop.html"
    context = {}

    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        med_form = MedicalshopRegistration(initial={"agent":AgentDetails.objects.get(user=request.user)})
        self.context["register_form"] = register_form
        self.context["med_form"] = med_form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user_reg = RegisterForm(request.POST)
        med_det = MedicalshopRegistration(request.POST)
        if user_reg.is_valid() and med_det.is_valid():
            print("valid")
            user = user_reg.save()
            user.user_type = "Medicalshop"
            user.save()
            med = med_det.save(commit=False)
            med.user = user
            med.save()
            messages.success(request,message="Registration Successful")
            return redirect("medicalshop-registration")
        else:
            print("invalid")
            messages.error(request, message="Invalid form data")
            self.context["register_form"] = user_reg
            self.context["med_form"] = med_det
            return render(request, self.template_name, self.context)


@method_decorator(agent_permission_required, name='dispatch')
class DoctorsAccountCreation(TemplateView):
    template_name = "medical/doc-reg.html"
    context = {}

    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        doc_form = DoctorRegistration(initial={"agent":AgentDetails.objects.get(user=request.user)})
        self.context["register_form"] = register_form
        self.context["doc_form"] = doc_form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user_reg = RegisterForm(request.POST)
        doc_det = DoctorRegistration(request.POST, request.FILES)
        if user_reg.is_valid() and doc_det.is_valid():
            print("valid")
            user = user_reg.save()
            user.user_type = "Doctor"
            user.save()
            doc = doc_det.save(commit=False)
            doc.user = user
            doc.save()
            messages.success(request,message="Registration successful")
            return redirect("doctors-registration")
        else:
            print("invalid")
            messages.error(request, message="Invalid form data")
            self.context["register_form"] = user_reg
            self.context["doc_form"] = doc_det
            return render(request, self.template_name, self.context)


@method_decorator(agent_permission_required, name='dispatch')
class PatientsAccountCreation(TemplateView):
    template_name = "medical/patient-reg.html"
    model = PatientDetails
    context = {}

    def get(self, request, *args, **kwargs):

        obj = self.model.objects.last()
        if obj:
            last_cardnum = obj.card_num
            card_num = int(last_cardnum) + 1

        else:
            card_num = 1
        date = timezone.now().date()
        agent=request.user
        print("agent ",agent)
        agent_obj=CustomUser.objects.get(username=agent)
        register_form = PatientRegistration(initial={"card_num": card_num,"date":date,"agent":AgentDetails.objects.get(user=request.user)})
        self.context["register_form"] = register_form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):

        patient_det = PatientRegistration(request.POST, request.FILES)
        if patient_det.is_valid():
            print("valid")
            patient_det.save()
            messages.success(request, message="Registration Successful")
            return redirect("patient-registration")
        else:
            print("invalid")
            messages.error(request, message="Invalid form data")
            self.context["register_form"] = patient_det
            return render(request, self.template_name, self.context)


def user_logout(req):
    logout(req)
    return redirect("landingpage")
