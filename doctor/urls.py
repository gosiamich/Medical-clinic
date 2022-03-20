"""doctor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from doctor_app.views import Index
from accounts.views import LoginView, LoginForm, LogOut, RegistrationView
from doctor_app.views import PatientRegistrationView, AddAppointmentView, ListViewPatient, \
    ListViewClinic, ListViewSpecialist, DetailViewClinic, UpdateViewClinic, ListViewSchedule

urlpatterns = [
    path('admin/', admin.site.urls, name= 'admin'),
    path('index/', Index.as_view(), name= 'index'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogOut.as_view(), name='logout'),
    path("registration/", RegistrationView.as_view(), name='u_registration'),
    path("pregistration/", PatientRegistrationView.as_view(), name='p_registration'),
    path('add_appointment/', AddAppointmentView.as_view(), name="add_appointment"),
    path('list_patients/', ListViewPatient.as_view(), name='list_patients'),
    path('list_clinics/', ListViewClinic.as_view(), name='list_clinics'),
    path('list_specialists/', ListViewSpecialist.as_view(), name='list_specialists'),
    path('detail_clinic/<int:pk>/', DetailViewClinic.as_view(), name='detail_clinic'),
    path('update_clinic/<int:pk>/', UpdateViewClinic.as_view(), name='update_clinic'),
    path('list_schedules/', ListViewSchedule.as_view(), name='list_schedules')
]
