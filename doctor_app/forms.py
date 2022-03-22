import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateTimeField
from django.forms.widgets import DateTimeInput

from doctor_app.models import Patient, Address, Clinic, Specialist, Type, TIME_SLOT, Visit


class CreatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['pesel', 'gender', 'phone_number']


class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


def check_date(a_date):
    if a_date < datetime.date.today():
        raise ValidationError("Choose actual date")


def ckeck_weekday(a_date):
    if a_date.isoweekday() > 5:
        raise ValidationError("Clinic is open from Monday to Friday")


def check_time(day_and_time):
    if day_and_time < datetime.time(10, 00, 00):
        raise ValidationError("Clinic starts at 10:00")
    if day_and_time > datetime.time(18, 00, 00):
        raise ValidationError("Clinic ends at 18:00")


class AddAppointmentForm(forms.Form):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    # day_and_time = forms.DateField(label='Choose a time for your appointment:', \
    #                                # validators=[check_date, ckeck_weekday, ],
    #                                widget=forms.DateTimeInput( \
    #                                    attrs={'type': 'datetime-local'}))
                                              # 'min': '2022-03-20T10:00:00', \
                                              # 'max': '2022-12-30T18:00:00', \
                                              # 'step': '1800'}))
    a_date = forms.DateField(label="Date", \
                             validators=[check_date, ckeck_weekday, ], \
                             widget=forms.DateInput(attrs={'type': 'date', }))
    a_time = forms.TimeField(label='Time:', \
                             help_text='Clinic hours 10-18', \
                             validators=[check_time, ], \
                             widget=forms.DateInput(
                                 attrs={'type': 'time', 'min': '10:00', 'max': '18:00', 'step': '1800'}, ))

    type = forms.ModelChoiceField(queryset=Type.objects.all())

    #
    # def clean(self):
    #     data = super().clean()
    #     errors = []
    #     if data['a_date'] < datetime.date.today():
    #         errors.append('invalid date')
