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

def check_time(a_from):
    if a_from < datetime.time(10, 00, 00):
        raise ValidationError("Clinic starts at 10:00")
    if a_from > datetime.time(18, 00, 00):
        raise ValidationError("Clinic ends at 18:00")


class AddAppointmentForm(forms.Form):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    a_date = forms.DateField(label="Data", validators=[check_date, ckeck_weekday, ])
    a_from = forms.TimeField(label='Time from:', validators=[check_time, ])
    # a_to = forms.TimeField(label='Time to:')
    type = forms.ModelChoiceField(queryset=Type.objects.all())

    #
    # def clean(self):
    #     data = super().clean()
    #     errors = []
    #     if data['a_date'] < datetime.date.today():
    #         errors.append('invalid date')


