import pytest
from django.contrib.auth.models import User, Permission

from doctor_app.models import Appointment, Clinic, Address, Specialization, Specialist, Schedule, Patient, Type


@pytest.fixture
def user():
    user = User.objects.create_user(username='gosia', password='gosia')
    vs = Permission.objects.get(codename='view_specialization')
    user.user_permissions.add(vs)
    vt = Permission.objects.get(codename='view_type')
    user.user_permissions.add(vt)
    cs = Permission.objects.get(codename='add_specialization')
    user.user_permissions.add(cs)
    ct = Permission.objects.get(codename='add_type')
    user.user_permissions.add(ct)
    return user

@pytest.fixture
def user2():
    return User.objects.create_user(username='user2', password='gosia', first_name = 'Spec')

@pytest.fixture
def superuser():
    return User.objects.create_superuser(username='gos', password='gosia')

@pytest.fixture
def address():
    return Address.objects.create(city='P', postcode='60-476', street='Dr', building_number='5')

@pytest.fixture
def type():
    return Type.objects.create(name='XXX')

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
def patient(user2, address):
    return Patient.objects.create(pesel='5258741258', gender = 'F', phone_number='55',address=address, user = user2 )

@pytest.fixture
def patients(user2, address):
    list =[]
    pat = Patient.objects.create(pesel='5258741258', gender = 'F', phone_number='55',address=address, user = user2 )
    list.append(pat)
    return list

@pytest.fixture
def clinics(address):
    list =[]
    clinic = Clinic.objects.create(name='Vision', phone_number='55',address=address, email = 'v@p.pl' )
    list.append(clinic)
    return list

@pytest.fixture
def specialists(address, user2, specialization):
    list =[]
    spec = Specialist.objects.create(user=user2, address=address, specialization=specialization,phone_number='5')
    list.append(spec)
    return list