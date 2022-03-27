import pytest
from django.contrib.auth.models import User

from doctor_app.models import Appointment, Clinic, Address, Specialization, Specialist, Schedule, Patient


@pytest.fixture
def user():
    return User.objects.create_user(username='gosia', password='gosia')

@pytest.fixture
def user2():
    return User.objects.create_user(username='user2', password='gosia', first_name = 'Spec')

@pytest.fixture
def superuser():
    return User.objects.create_user(username='gosia', password='gosia', is_superuser= True)

@pytest.fixture
def address():
    return Address.objects.create(city='P', postcode='60-476', street='Dr', building_number='5')

@pytest.fixture
def clinic(address):
    return Clinic.objects.create(name='Lux',phone_number='5', email='l@p.pl', address=address )

@pytest.fixture
def specialization():
    return Specialization.objects.create(name='Optometrist')

@pytest.fixture
def specialist(address, user2, specialization):
    return Specialist.objects.create(user=user2, address=address, specialization=specialization,phone_number='5')

@pytest.fixture
def schedules(clinic, specialist):
    list =[]
    sch = Schedule.objects.create(day_of_week='1', sch_to='10:00', sch_from='15:00',clinic=clinic, specialist=specialist)
    list.append(sch)
    return list

@pytest.fixture
def patients(user2, address):
    list =[]
    pat = Patient.objects.create(pesel='5258741258', gender = 'F', phone_number='55',address=address, user = user2 )
    list.append(pat)
    return list