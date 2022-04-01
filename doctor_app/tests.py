from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
import pytest

# Create your tests here.
from django.urls import reverse
from freezegun import freeze_time

from accounts.forms import CreateUserForm
from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm, CreateSpecialistForm, \
    CreateClinicForm
from doctor_app.models import Patient, Specialization, Specialist, Schedule, Appointment, Address, WEEK_DAY, Clinic, \
    Type


# Create your tests here.

@pytest.mark.django_db
def test_index():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_registration_get():
    client = Client()
    url = reverse('p_registration')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'],CreateUserForm)
    assert isinstance(response.context['model_form'], CreatePatientForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)

@pytest.mark.django_db
def test_PatientRegistrationView_post():
    client = Client()
    url = reverse('p_registration')
    date = {
        'username': 'gos',
        'password':'goog',
        'first_name':'gos',
        'last_name':'mic',
        'email':'gm@p.pl',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
        'pesel': '5854745852',
        'gender': 'F',
        'phone_number':'55',
            }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('index')
    assert response.url.startswith(new_url)
    Patient.objects.get(pesel='5854745852')



@pytest.mark.django_db
def test_ModifyUserPatientFORM_post(user2, patient):
    client = Client()
    client.force_login(user2)
    url = reverse('modify_user')
    date = {
        'username': 'Gosss',
        'password':'goog',
        'first_name':'gos',
        'last_name':'mic',
        'email':'gm@p.pl',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
        'pesel': '5854745852',
        'gender': 'F',
        'phone_number':'55',
            }
    response = client.post(url, date)
    User.objects.get(username='Gosss')

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

@freeze_time('2022-03-31 00:00:00')
@pytest.mark.django_db
def test_add_appointment_post(user2, patient, clinic, specialist, type):
    client = Client()
    client.force_login(user2)
    url = reverse('add_appointment')
    date = {
        'clinic': clinic.id,
        'specialist': specialist.id,
        'a_date':'2022-04-04',
        'a_time': '12:30',
        'type': type.id,
    }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('index')
    assert response.url.startswith(new_url)
    Appointment.objects.get(**date)

@pytest.mark.django_db
def test_CreateClinicView_not_login():
    client = Client()
    url = reverse('create_clinic')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_CreateClinicView_get_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_clinic')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['model_form'], CreateClinicForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)



@pytest.mark.django_db
def test_CreateClinicView_post(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_clinic')
    data = {
        'name': 'Luxmed',
        'email': 'lm@p.pl',
        'phone_number':'55',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('list_clinics')
    assert response.url.startswith(new_url)
    Clinic.objects.get(name='Luxmed')



@pytest.mark.django_db
def test_ModifyClinicFORM_get_not_login(clinic):
    client = Client()
    url = reverse('modify_clinic', args=(clinic.id,))
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_ModifyClinicFORM_get_login_without_perm(user2,clinic):
    client = Client()
    client.force_login(user2)
    url = reverse('modify_clinic', args=(clinic.id,))
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_ModifyClinicFORM_post(user, clinic):
    client = Client()
    client.force_login(user)
    url = reverse('modify_clinic', args=(clinic.id,))
    data = {
        'name': 'LUXXX',
        'email': 'lm@p.pl',
        'phone_number':'55',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
    }
    response = client.post(url, data)
    Clinic.objects.get(name="LUXXX")

@pytest.mark.django_db
def test_DetailViewClinic(clinic):
    client = Client()                  
    url = reverse('detail_clinic', args=(clinic.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object'].name == clinic.name


@pytest.mark.django_db
def test_CreateSpecialistView_not_login():
    client = Client()
    url = reverse('create_specialist')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_CreateSpecialistView_get_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_specialist')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CreateUserForm)
    assert isinstance(response.context['model_form'], CreateSpecialistForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)



@pytest.mark.django_db
def test_CreateViewSchedule_post(superuser,clinic, specialist):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_schedule')
    data = {
        'day_of_week': '1',
        'sch_from': '10:00',
        'sch_to': '15:00',
        'clinic': clinic.id,
        'specialist': specialist.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('list_schedules')
    assert response.url.startswith(new_url)
    Schedule.objects.get(**data)


@pytest.mark.django_db
def test_CreateSpecialistView_post(superuser, specialization):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_specialist')
    data = {
        'username': 'gos2',
        'password':'goog',
        'first_name':'gos',
        'last_name':'mic',
        'email':'gm@p.pl',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
        'specialization': specialization.id,
        'phone_number':'55',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('list_specialists')
    assert response.url.startswith(new_url)
    Specialist.objects.get(user__username='gos2')


@pytest.mark.django_db
def test_CreateViewSchedule_not_login():
    client = Client()
    url = reverse('create_schedule')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_CreateViewSchedule_post(superuser,clinic, specialist):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_schedule')
    data = {
        'day_of_week': '1',
        'sch_from': '10:00',
        'sch_to': '15:00',
        'clinic': clinic.id,
        'specialist': specialist.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('list_schedules')
    assert response.url.startswith(new_url)
    Schedule.objects.get(**data)

@pytest.mark.django_db
def test_UpdateViewSchedule_get_not_login(schedules):
    schedule = schedules[0]
    client = Client()
    url = reverse('update_schedule', args=(schedule.id,))
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_UpdateViewSchedule_get_login_without_perm(user2,schedules):
    schedule = schedules[0]
    client = Client()
    client.force_login(user2)
    url = reverse('update_schedule', args=(schedule.id,))
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_UpdateViewSchedule_get_login_with_perm(user,schedules):
    schedule = schedules[0]
    client = Client()
    client.force_login(user)
    url = reverse('update_schedule', args=(schedule.id,))
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_UpdateViewSchedule_post_login_with_perm(user, schedules, clinic, specialist):
    schedule = schedules[0]
    client = Client()
    client.force_login(user)
    url = reverse('update_schedule', args=(schedule.id,))
    data = {
        'day_of_week': '5',
        'sch_from': '10:00',
        'sch_to': '15:00',
        'clinic': clinic.id,
        'specialist': specialist.id,
    }
    response = client.post(url, data)
    Schedule.objects.get(day_of_week='5')


@pytest.mark.django_db
def test_CreateViewType_get_not_login():
    client = Client()
    url = reverse('create_type')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_CreateViewType_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('create_type')
    date = {
        'name': 'Evrything',
    }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('list_types')
    assert response.url.startswith(new_url)
    Type.objects.get(**date)


@pytest.mark.django_db
def test_CreateViewSpecialization_not_login():
    client = Client()
    url = reverse('create_specialization')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_CreateViewSpecialization_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('create_specialization')
    date = {
        'name': 'Opto',
    }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('list_specializations')
    assert response.url.startswith(new_url)
    Specialization.objects.get(**date)

@pytest.mark.django_db
def test_ListViewSchedule_not_login():
    client = Client()
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_ListViewSchedule_login_without_perm(user2):
    client = Client()
    client.force_login(user2)
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_ListViewSchedule_login_with_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0


@pytest.mark.django_db
def test_ListViewSchedule_login(user, schedules):
    client = Client()
    client.force_login(user)
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(schedules)
    for sch in schedules:
        assert sch in response.context['object_list']


@pytest.mark.django_db
def test_ListViewPatient_not_login():
    client = Client()
    url = reverse('list_patients')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_ListViewPatient_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('list_patients')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0

@pytest.mark.django_db
def test_ListViewPatient_login(superuser, patients):
    client = Client()
    client.force_login(superuser)
    url = reverse('list_patients')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(patients)
    for pat in patients:
        assert pat in response.context['object_list']


@pytest.mark.django_db
def test_ListViewClinic(clinics):
    client = Client()
    url = reverse('list_clinics')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(clinics)
    for clinic in clinics:
        assert clinic in response.context['object_list']


@pytest.mark.django_db
def test_ListViewspecialists(specialists):
    client = Client()
    url = reverse('list_specialists')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(specialists)
    for spec in specialists:
        assert spec in response.context['object_list']

@pytest.mark.django_db
def test_ListViewSpecialization_not_login():
    client = Client()
    url = reverse('list_specializations')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_ListViewSpecialization_login_without_perm(user2):
    client = Client()
    client.force_login(user2)
    url = reverse('list_specializations')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_ListViewSpecialization_login_with_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('list_specializations')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0


@pytest.mark.django_db
def test_ListViewType_not_login():
    client = Client()
    url = reverse('list_types')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_ListViewType_login_without_perm(user2):
    client = Client()
    client.force_login(user2)
    url = reverse('list_types')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_ListViewType_login_with_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('list_types')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0


@pytest.mark.django_db
def test_DeleteViewSchedule_not_login(schedules):
    schedule = schedules[0]
    client = Client()
    url = reverse('delete_schedule', args=(schedule.id,))
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_DeleteViewSchedule_login_without_perm(user2, schedules):
    schedule = schedules[0]
    client = Client()
    client.force_login(user2)
    url = reverse('delete_schedule', args=(schedule.id,))
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_DeleteViewSchedule_login_with_perm(user, schedules):
    schedule = schedules[0]
    client = Client()
    client.force_login(user)
    url = reverse('delete_schedule', args=(schedule.id,))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_DeleteViewAppointment_not_login(appointment):
    client = Client()
    url = reverse('delete_appointment', args=(appointment.id,))
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_DeleteViewAppointment_login_without_perm(user2, appointment):
    client = Client()
    client.force_login(user2)
    url = reverse('delete_appointment', args=(appointment.id,))
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_DeleteViewAppointment_login_with_perm(user, appointment):
    client = Client()
    client.force_login(user)
    url = reverse('delete_appointment', args=(appointment.id,))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_DeleteViewAppointment_post_login_with_permission(user, appointment):
    client = Client()
    client.force_login(user)
    url = reverse('delete_appointment', args=(appointment.id,))
    response = client.post(url)
    assert response.status_code == 302
    new_url = reverse('list_appointments')
    assert response.url.startswith(new_url)
    with pytest.raises(Appointment.DoesNotExist):
        Appointment.objects.get(id=appointment.id)

# ???????????????????????