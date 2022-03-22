import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm
from accounts.forms import CreateUserForm
from doctor_app.models import Appointment, Schedule, Patient, Clinic, Specialist


class Index(View):
    def get(self, request):
        return render(request, "doctor_app/index.html", )


class PatientRegistrationView(View):

    def get(self, request):
        form = CreateUserForm()
        patient_form = CreatePatientForm()
        address_form = CreateAddressForm()
        return render(request, 'doctor_app/registration.html',
                      {'form': form, 'patient_form': patient_form, 'address_form': address_form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        patient_form = CreatePatientForm(request.POST)
        address_form = CreateAddressForm(request.POST)
        if form.is_valid() and patient_form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = address_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.address = address
            patient.save()
            message = f'Thank Yoy for registration. Now You can make an appointment'
            return render(request, 'doctor_app/index.html', {'message': message})
        return render(request, 'doctor_app/registration.html',
                      {'form': form, 'patient_form': patient_form, 'address_form': address_form})


class AddAppointmentView(View):

    def get(self, request):
        form = AddAppointmentForm()
        return render(request, 'doctor_app/form.html', {'form': form})

    def post(self, request):
        form = AddAppointmentForm(request.POST)
        if form.is_valid():
            clinic = form.cleaned_data['clinic']
            specialist = form.cleaned_data['specialist']
            # day_and_time = form.cleaned_data['day_and_time']
            a_date = form.cleaned_data['a_date']
            a_time = form.cleaned_data['a_time']
            # a_to = form.cleaned_data['a_to']
            type = form.cleaned_data['type']
            user = User.objects.get(pk=request.user.id)
            patient_id = user.patient.id
            schedule = Schedule.objects.filter(clinic=clinic, specialist=specialist, day_of_week=a_date.isoweekday(), \
                                           sch_from__lte=a_time, sch_to__gt=a_time)
            if not schedule:
                schedule = Schedule.objects.get(clinic=clinic, specialist=specialist, day_of_week=a_date.isoweekday())
                return render(request, 'doctor_app/form.html',
                              {'form': form, 'message': f'{schedule.specialist} {a_date} przyjmuje od {schedule.sch_from} do {schedule.sch_to}'})
            else:
                if len(Appointment.objects.filter(a_date=a_date, a_time=a_time, specialist=specialist)) > 0:
                    list_busy_time =[]
                    for a in Appointment.objects.filter(a_date=a_date, specialist=specialist):
                        list_busy_time.append(a.a_time)
                    return render(request, 'doctor_app/form.html', {'form': form,'message': f'{specialist} {a_date} ma zajęte godziny: {list_busy_time}'})
                else:
                    Appointment.objects.create(a_date=a_date, a_time=a_time, specialist=specialist, clinic=clinic,patient_id =patient_id, type=type)
                    return render(request, "doctor_app/index.html", {'message':f'brawo wizyta zarezerwowana'})
        return render(request, 'doctor_app/form.html', {'form': form})


class ListViewPatient(ListView):
    model = Patient
    template_name = 'doctor_app/list_patients.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ListViewPatient, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['message'] = 'This is just some data from extra context'
        return context


class ListViewClinic(ListView):
    model = Clinic
    template_name = 'doctor_app/list_clinics.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ListViewClinic, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['message'] = 'List of Clinics:.'
        return context


class ListViewSpecialist(ListView):
    model = Specialist
    template_name = 'doctor_app/list_specialists.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ListViewSpecialist, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['message'] = 'List of Specialists:.'
        return context


class ListViewSchedule(ListView):
    model = Schedule
    template_name = 'doctor_app/list_schedules.html'


class DetailViewClinic(DetailView):
    model = Clinic
    template_name = 'doctor_app/detail_clinic.html'


class UpdateViewClinic(UpdateView):
    model = Clinic
    fields = ['name', 'phone_number', 'email']
    success_url = reverse_lazy('list_clinics')
    template_name = 'doctor_app/form.html'
