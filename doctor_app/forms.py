import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateTimeField
from django.forms.widgets import DateTimeInput
from numpy import sort

from doctor_app.models import Patient, Address, Clinic, Specialist, Type, TIME_SLOT, Visit, Schedule, Appointment


class CreatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['pesel', 'gender', 'phone_number']


class CreateClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'email', 'phone_number']


class CreateSpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        fields = ['specialization', 'phone_number']


def PostcodeValidate(postcode):
    s = postcode.replace(" ", "")
    if not len(s) == 6:
        raise ValidationError('Wrong poscode')
    else:
        if not s[2] == '-':
            raise ValidationError('Wrong postcode')
        else:
            s = s.replace("-", "")
            for i in range(len(s)):
                if not(s[i].isdigit()):
                    raise ValidationError('Wrong postcode')
            else:
                return True



class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


    def clean_postcode(self):
        if not PostcodeValidate(self.cleaned_data['postcode']):
            raise ValidationError('Wrong postcode')
        return self.cleaned_data['postcode']


def check_date(a_date):
    if a_date < datetime.date.today():
        raise ValidationError("Choose actual date")


def ckeck_weekday(a_date):
    if a_date.isoweekday() > 5:
        raise ValidationError("Clinic is open from Monday to Friday")


class AddAppointmentForm(forms.Form):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    specialist = forms.ModelChoiceField(queryset=Specialist.objects.all())
    a_date = forms.DateField(label="Date",
                             validators=[check_date, ckeck_weekday, ],
                             widget=forms.DateInput(attrs={'type': 'date', }))
    a_time = forms.TimeField(label='Time:', \
                              help_text='Clinic hours 10-18', \
                             widget=forms.DateInput(
                                 attrs={'type': 'time', 'min': '10:00', 'max': '18:00', 'step': '1800'}, ))

    type = forms.ModelChoiceField(queryset=Type.objects.all())

    def clean(self):
        data = super().clean()
        errors = []
        if not 'a_date' in data:
            return data
        if data['a_date'] == datetime.date.today() and data['a_time'] < datetime.datetime.now().time():
            errors.append('podaj godzinę późnejszą niz aktualna!')
            raise forms.ValidationError(errors)
        if len(Schedule.objects.filter(clinic=data['clinic'], specialist=data['specialist']))==0:
            errors.append('specjalista w tej przychodni nie przyjmuje!')
            raise forms.ValidationError(errors)
        else:
            if len(Schedule.objects.filter(clinic=data['clinic'], specialist=data['specialist'],
                                       day_of_week=data['a_date'].isoweekday())) == 0:
                errors.append('specjalista w tym dniu nie przyjmuje!')
                raise forms.ValidationError(errors)
            else:
                if len(Schedule.objects.filter(clinic=data['clinic'], specialist=data['specialist'],
                                       day_of_week=data['a_date'].isoweekday(),\
                                        sch_from__lte=data['a_time'], sch_to__gt=data['a_time'])) == 0:
                    errors.append('specjalista w tym dniu o tej godzinie nie przyjmuje!')
                    raise forms.ValidationError(errors)
                else:
                    if len(Appointment.objects.filter(a_date=data['a_date'], a_time=data['a_time'],
                                              specialist=data['specialist'])) > 0:
                        list_busy_time = []
                        for a in Appointment.objects.filter(a_date=data['a_date'], specialist=data['specialist']):
                            time_format = a.a_time.strftime("%H:%M")
                            list_busy_time.append(time_format)
                        errors.append(f'specjalista ma zajęte godziny: {sort(list_busy_time)})')
                        raise forms.ValidationError(errors)




