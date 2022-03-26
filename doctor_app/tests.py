from django.test import TestCase
from django.test import Client
import pytest

# Create your tests here.
from django.urls import reverse

from accounts.forms import CreateUserForm
from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm
from doctor_app.models import Patient, Specialization,Specialist, Schedule,Appointment,Address,WEEK_DAY

# Create your tests here.

@pytest.mark.django_db
def test_index():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_registration():
    client = Client()
    url = reverse('p_registration')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_registration_get():
    client = Client()
    url = reverse('p_registration')
    response = client.get(url)
    assert isinstance(response.context['form'],CreateUserForm)
    assert isinstance(response.context['patient_form'], CreatePatientForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)

@pytest.mark.django_db
def test_add_appointment_not_login():
    client = Client()
    url = reverse('add_appointment')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_add_appointment_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_appointment')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddAppointmentForm)

@pytest.mark.django_db
def test_add_appointment_post():
    client = Client()
    url = reverse('add_appointment')
    date = {
        'clinic': '1',
        'specialist': '1',
        'a_date':'2022-3-28',
        'a_time': '12:30',
        'type': '1',
         'patient_id': '1'
    }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('index')
    assert response.url.startswith(new_url)
    Appointment.objects.get(clinic='1')

