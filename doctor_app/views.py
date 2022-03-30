import datetime
from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm, CreateSpecialistForm, \
    CreateClinicForm
from accounts.forms import CreateUserForm
from doctor_app.models import Appointment, Schedule, Patient, Clinic, Specialist, Address, Type, Specialization
from django.contrib.auth.models import User

# 1
class Index(View):
    def get(self, request):
        return render(request, "doctor_app/index.html")

# 2
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

#3
class PatientRegistrationView(View):

    def get(self, request):
        form = CreateUserForm()
        model_form = CreatePatientForm()
        address_form = CreateAddressForm()
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form,\
                       'address_form': address_form, 'message': 'Register as a Patient'})

    def post(self, request):
        form = CreateUserForm(request.POST)
        model_form = CreatePatientForm(request.POST)
        address_form = CreateAddressForm(request.POST)
        if form.is_valid() and model_form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = address_form.save()
            patient = model_form.save(commit=False)
            patient.user = user
            patient.address = address
            patient.save()
            # message = f'Thank Yoy for registration. Now You can make an appointment'
            return redirect( 'index')
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form, 'address_form': address_form})

#4
class CreateSpecialistView(SuperuserRequiredMixin, View):
    def get(self, request):
        form = CreateUserForm()
        model_form = CreateSpecialistForm()
        address_form = CreateAddressForm()
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form, \
                       'address_form': address_form, 'message': 'CREATE NEW SPECIALIST:'})

    def post(self, request):
        form = CreateUserForm(request.POST)
        model_form = CreateSpecialistForm(request.POST)
        address_form = CreateAddressForm(request.POST)
        if form.is_valid() and model_form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = address_form.save()
            specialist = model_form.save(commit=False)
            specialist.user = user
            specialist.address = address
            specialist.save()
            return redirect('list_specialists')
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form, 'address_form': address_form})

#5
class CreateClinicView(SuperuserRequiredMixin, View):
    def get(self, request):
        model_form = CreateClinicForm()
        address_form = CreateAddressForm()
        return render(request, 'doctor_app/form.html',
                      {'model_form': model_form, \
                       'address_form': address_form, 'message': 'CREATE NEW CLINIC:'})

    def post(self, request):
        model_form = CreateClinicForm(request.POST)
        address_form = CreateAddressForm(request.POST)
        if model_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            clinic = model_form.save(commit=False)
            clinic.address = address
            clinic.save()
            return redirect('list_clinics')
        return render(request, 'doctor_app/form.html',
                      {'model_form': model_form, 'address_form': address_form, 'message': 'Try again (NEW CLINIC)' })

#6
class CreateViewSchedule(SuperuserRequiredMixin,CreateView):
    model = Schedule
    fields = '__all__'
    success_url = reverse_lazy('list_schedules')
    template_name = 'doctor_app/create_schedule.html'

#7
class AddAppointmentView(LoginRequiredMixin, View):

    def get(self, request):
        form = AddAppointmentForm()
        return render(request, 'doctor_app/form.html', {'form': form})

    def post(self, request):
        form = AddAppointmentForm(request.POST)
        if form.is_valid():
            clinic = form.cleaned_data['clinic']
            specialist = form.cleaned_data['specialist']
            a_date = form.cleaned_data['a_date']
            a_time = form.cleaned_data['a_time']
            type = form.cleaned_data['type']
            user = User.objects.get(pk=request.user.id)
            patient_id = user.patient.id
            Appointment.objects.create(a_date=a_date, a_time=a_time, specialist=specialist, clinic=clinic,
                                               patient_id=patient_id, type=type)
            return redirect('index')
            # return render(request, "doctor_app/index.html", {'message': f'brawo wizyta zarezerwowana'})
        return render(request, 'doctor_app/form.html', {'form': form})

#8
class ListViewPatient(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_patient']
    model = Patient
    template_name = 'doctor_app/list_patients.html'

#9
class ListViewClinic(ListView):
    model = Clinic
    template_name = 'doctor_app/list_clinics.html'

# 10
class ListViewSpecialist(ListView):
    model = Specialist
    template_name = 'doctor_app/list_specialists.html'

# 11
class ListViewSchedule(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_schedule']
    model = Schedule
    template_name = 'doctor_app/list_schedules.html'

# 12
class ListViewAppointment(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'doctor_app/list_appointments.html'
# 13
class DetailViewClinic(DetailView):
    model = Clinic
    template_name = 'doctor_app/detail_clinic.html'

# 14
class ModifyUserPatientFORM(LoginRequiredMixin, View):
    # only Patient may change its own data
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        patient = Patient.objects.get(user=user)
        model_form = CreatePatientForm(instance = patient)
        form = CreateUserForm(instance = user)
        address_form = CreateAddressForm(instance = patient.address)
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form,\
                       'address_form': address_form, 'message': 'Modify Your date:'})

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        patient = Patient.objects.get(user=user)
        form = CreateUserForm(request.POST, instance = user)
        model_form = CreatePatientForm(request.POST, instance=patient)
        address_form = CreateAddressForm(request.POST, instance= patient.address)
        if form.is_valid() and model_form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = address_form.save()
            patient = model_form.save(commit=False)
            patient.user = user
            patient.address = address
            patient.save()
            return redirect('index')
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form, 'address_form': address_form, 'message': 'Try again..'})

# 15
class ModifyUserSpecialistFORM(PermissionRequiredMixin, View):
    permission_required = ['doctor_app.change_specialist']
    # only Specialist may change its own data
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        specialist = Specialist.objects.get(user=user)
        model_form = CreateSpecialistForm(instance = specialist)
        form = CreateUserForm(instance = user)
        address_form = CreateAddressForm(instance = specialist.address)
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form,\
                       'address_form': address_form, 'message': 'Modify Your data:'})

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        specialist = Specialist.objects.get(user=user)
        form = CreateUserForm(request.POST, instance = user)
        model_form = CreateSpecialistForm(request.POST, instance=specialist)
        address_form = CreateAddressForm(request.POST, instance= specialist.address)
        if form.is_valid() and model_form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = address_form.save()
            specialist = model_form.save(commit=False)
            specialist.user = user
            specialist.address = address
            specialist.save()
            return redirect('index')
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form, 'address_form': address_form, 'message': 'Try again..'})

# 16
class ModifyClinicFORM(PermissionRequiredMixin, View):
    permission_required = ['doctor_app.change_clinic']
    def get(self, request, pk):
        clinic = Clinic.objects.get(id=pk)
        model_form = CreateClinicForm(instance= clinic)
        address_form = CreateAddressForm(instance = clinic.address)
        return render(request, 'doctor_app/form.html',
                      {'model_form': model_form, 'address_form': address_form, 'message': 'Update CLINIC:'})
    def post(self, request, pk):
        clinic = Clinic.objects.get(id=pk)
        m_form = CreateClinicForm(request.POST, instance = clinic)
        a_form = CreateAddressForm(request.POST, instance = clinic.address)
        if m_form.is_valid() and a_form.is_valid():
            address = a_form.save()
            clinic = m_form.save(commit=False)
            clinic.address = address
            clinic.save()
            return redirect('list_clinics')

# 17
class UpdateViewSchedule(PermissionRequiredMixin, UpdateView):
    permission_required = ['doctor_app.change_schedule']
    model = Schedule
    fields = '__all__'
    success_url = reverse_lazy('list_schedules')
    template_name = 'doctor_app/form.html'

# 18
class DeleteViewSchedule(PermissionRequiredMixin, DeleteView):
    permission_required = ['doctor_app.delete_schedule']
    model = Schedule
    success_url = '/list_schedules/'

# 19
class DeleteViewAppointment(PermissionRequiredMixin, DeleteView):
    permission_required = ['doctor_app.delete_appointment']
    model = Appointment
    success_url = '/list_appointments/'

#20
class CreateViewType(PermissionRequiredMixin, CreateView):
    permission_required = ['doctor_app.add_type']
    model = Type
    fields = '__all__'
    success_url = reverse_lazy("list_types")
    template_name = 'doctor_app/create_type.html'

# 21
class ListViewType(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_type']
    model = Type
    template_name = 'doctor_app/list_types.html'

# 22
class CreateViewSpecialization(PermissionRequiredMixin, CreateView):
    permission_required = ['doctor_app.add_specialization']
    model = Specialization
    fields = '__all__'
    success_url = reverse_lazy('list_specializations')
    template_name = 'doctor_app/create_specialization.html'

# 23
class ListViewSpecialization(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_specialization']
    model = Specialization
    template_name = 'doctor_app/list_specialization.html'
