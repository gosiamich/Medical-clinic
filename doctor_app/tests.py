from django.test import TestCase
from django.test import Client
import pytest

# Create your tests here.
from django.urls import reverse

from accounts.forms import CreateUserForm
from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm
from doctor_app.models import Patient, Specialization,Specialist, Schedule,Appointment,Address,WEEK_DAY
from django.test import TestCase

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