import datetime
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm, CreateSpecialistForm, \
    CreateClinicForm, SearchForm
from accounts.forms import CreateUserForm
from doctor_app.models import Appointment, Schedule, Patient, Clinic, Specialist, Address, Type, Specialization
from django.contrib.auth.models import User
from django.db.models import Q


class Index(View):
    def get(self, request):
        return render(request, "doctor_app/index.html")


class Aboute(View):
    def get(self, request):
        return render(request, "doctor_app/aboute.html")


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


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
            return redirect( 'index')
        return render(request, 'doctor_app/form.html',
                      {'form': form, 'model_form': model_form, 'address_form': address_form})


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


class CreateViewSchedule(SuperuserRequiredMixin,CreateView):
    model = Schedule
    fields = '__all__'
    success_url = reverse_lazy('list_schedules')
    template_name = 'doctor_app/create_schedule.html'


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
            # request.session['message'] = f'Your appointment: {a_date}  at {a_time} with specialist: {specialist} in {clinic}'
            return redirect('list_user_appointments')
        return render(request, 'doctor_app/form.html', {'form': form})



class ListViewClinic(ListView):
    model = Clinic
    template_name = 'doctor_app/list_clinics.html'


class ListViewSpecialist(ListView):
    model = Specialist
    template_name = 'doctor_app/list_specialists.html'


class ListViewSchedule(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_schedule']
    model = Schedule
    template_name = 'doctor_app/list_schedules.html'
    ordering = ['specialist', 'day_of_week']


class DetailViewClinic(DetailView):
    model = Clinic
    template_name = 'doctor_app/detail_clinic.html'


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


class UpdateViewSchedule(PermissionRequiredMixin, UpdateView):
    permission_required = ['doctor_app.change_schedule']
    model = Schedule
    fields = '__all__'
    success_url = reverse_lazy('list_schedules')
    template_name = 'doctor_app/form.html'


class DeleteViewSchedule(PermissionRequiredMixin, DeleteView):
    permission_required = ['doctor_app.delete_schedule']
    model = Schedule
    success_url = '/list_schedules/'


class DeleteViewAppointment(PermissionRequiredMixin, DeleteView):
    permission_required = ['doctor_app.delete_appointment']
    model = Appointment
    success_url = '/list_appointments/'


class CreateViewType(PermissionRequiredMixin, CreateView):
    permission_required = ['doctor_app.add_type']
    model = Type
    fields = '__all__'
    success_url = reverse_lazy("list_types")
    template_name = 'doctor_app/create_type.html'


class ListViewType(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_type']
    model = Type
    template_name = 'doctor_app/list_types.html'


class CreateViewSpecialization(PermissionRequiredMixin, CreateView):
    permission_required = ['doctor_app.add_specialization']
    model = Specialization
    fields = '__all__'
    success_url = reverse_lazy('list_specializations')
    template_name = 'doctor_app/create_specialization.html'


class ListViewSpecialization(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_specialization']
    model = Specialization
    template_name = 'doctor_app/list_specialization.html'


class ListSpecialistSchedule(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_schedule']
    model = Schedule
    template_name = 'doctor_app/list_schedules.html'

    def get_queryset(self):
        if len(Specialist.objects.filter(user=self.request.user.id)) == 0:
            object_list = Schedule.objects.all().order_by('day_of_week')
        else:
            object_list = Schedule.objects.filter(specialist=Specialist.objects.get(user=self.request.user.id)).order_by('day_of_week')
        return object_list



class DetailViewSpecialist(DetailView):
    model = Specialist
    template_name = 'doctor_app/detail_specialist.html'


class ListAppointment(SuperuserRequiredMixin, View):

    def get(self,request):
        object_list = Appointment.objects.all().order_by('a_date', 'a_time')
        return render(request, 'doctor_app/list_appointments.html', {'object_list': object_list})

    def post(self, request):
        choice = request.POST.get("app")
        if choice == "Actual":
            object_list = Appointment.objects.filter(a_date__gte=datetime.date.today()).order_by('a_date', 'a_time')
        elif choice == 'Archival':
            object_list = Appointment.objects.filter(a_date__lt=datetime.date.today()).order_by('a_date', 'a_time')
        elif choice == 'All':
            object_list = Appointment.objects.all().order_by('a_date', 'a_time')
        else:
            raise Exception('something is wrong :(')
        return render(request, 'doctor_app/list_appointments.html', {'object_list': object_list})



class ListUserAppointment(LoginRequiredMixin, View):

    def get(self, request):
        specialist = Specialist.objects.filter(user=self.request.user.id)
        if len(specialist) >0:
            object_list = Appointment.objects.filter(specialist=Specialist.objects.get(user=self.request.user.id)).\
            order_by('a_date', 'a_time')
        else:
            object_list = Appointment.objects.filter(patient=Patient.objects.get(user=self.request.user.id)). \
                order_by('a_date', 'a_time')
        return render(request, 'doctor_app/list_appointments.html',{'object_list': object_list})

    def post(self, request):
        choice = request.POST.get("app")
        specialist = Specialist.objects.filter(user=self.request.user.id)
        patient = Patient.objects.get(user=self.request.user.id)
        if len(specialist) > 0:
            appointments = Appointment.objects.filter(specialist=specialist).order_by('a_date', 'a_time')
        else:
            appointments = Appointment.objects.filter(patien=patient).order_by('a_date', 'a_time')
        if choice == "Actual":
            object_list = appointments.filter(a_date__gte=datetime.date.today())
        elif choice == 'Archival':
            object_list = appointments.filter(a_date__lt=datetime.date.today())
        elif choice == 'All':
            object_list = appointments
        else:
                raise Exception('something is wrong :(')
        return render(request, 'doctor_app/list_appointments.html',{'object_list': object_list})


class ListViewPatient(PermissionRequiredMixin, ListView):
    permission_required = ['doctor_app.view_patient']
    model = Patient
    template_name = 'doctor_app/list_patients.html'


class ListSearchPatientView(SuperuserRequiredMixin,View):

    def get(self, request):
        form = SearchForm()
        object_list = Patient.objects.all()
        return render(request, 'doctor_app/search_form.html', {'form': form, 'object_list':object_list})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            object_list = Patient.objects.filter( Q(pesel__icontains=search)\
                                                 | Q(user__username__icontains=search)\
                                                    | Q(user__last_name__icontains=search)\
                                                    | Q(user__first_name__icontains=search))
            return render(request, 'doctor_app/search_form.html',
                              {'form': form,'object_list':object_list})
        return render(request, 'doctor_app/form.html', {'form': form})

