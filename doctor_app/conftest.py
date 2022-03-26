import pytest
from django.contrib.auth.models import User

from doctor_app.models import Appointment

@pytest.fixture
def user():
    return User.objects.create_user(username='gosia', password='gosia')