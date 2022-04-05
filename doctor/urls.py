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
from accounts.views import LoginView, LoginForm, LogOut, RegistrationView
from doctor_app.views import Index, Aboute, PatientRegistrationView, AddAppointmentView, ListViewPatient, \
    ListViewClinic, ListViewSpecialist, DetailViewClinic, ListViewSchedule,\
    ListAppointment, DeleteViewAppointment, CreateViewSchedule, UpdateViewSchedule, DeleteViewSchedule,\
    CreateSpecialistView, CreateClinicView, ModifyClinicFORM, ModifyUserPatientFORM, ModifyUserSpecialistFORM,\
    CreateViewType, CreateViewSpecialization, ListViewType, ListViewSpecialization, ListSpecialistSchedule,\
    DetailViewSpecialist, ListUserAppointment


urlpatterns = [
    path('admin/', admin.site.urls, name= 'admin'),
    path('', Index.as_view(), name= 'index'),
    path('aboute/', Aboute.as_view(), name = 'aboute'),
    path("accounts/login/", LoginView.as_view(), name='login'),
    path("logout/", LogOut.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='u_registration'),
    path('pregistration/', PatientRegistrationView.as_view(), name='p_registration'),
    path('add_appointment/', AddAppointmentView.as_view(), name="add_appointment"),
    path('list_patients/', ListViewPatient.as_view(), name='list_patients'),
    path('list_clinics/', ListViewClinic.as_view(), name='list_clinics'),
    path('list_specialists/', ListViewSpecialist.as_view(), name='list_specialists'),
    path('detail_clinic/<int:pk>/', DetailViewClinic.as_view(), name='detail_clinic'),
    path('list_schedules/', ListViewSchedule.as_view(), name='list_schedules'),
    path('list_appointments/', ListAppointment.as_view(), name='list_appointments'),
    path('delete_appointment/<int:pk>/', DeleteViewAppointment.as_view(), name='delete_appointment'),
    path('create_schedule/', CreateViewSchedule.as_view(), name='create_schedule'),
    path('update_schedule/<int:pk>/',UpdateViewSchedule.as_view(), name='update_schedule'),
    path('delete_schedule/<int:pk>/', DeleteViewSchedule.as_view(), name='delete_schedule'),
    path('create_specialist/', CreateSpecialistView.as_view(), name= 'create_specialist'),
    path('create_clinic/', CreateClinicView.as_view(), name ='create_clinic'),
    path('modify_clinic/<int:pk>/', ModifyClinicFORM.as_view(), name='modify_clinic'),
    path('modify_user/', ModifyUserPatientFORM.as_view(), name='modify_user'),
    path('modify_specialist/', ModifyUserSpecialistFORM.as_view(), name='modify_specialist'),
    path('create_type/', CreateViewType.as_view(), name='create_type'),
    path('create_specialization/', CreateViewSpecialization.as_view(), name='create_specialization'),
    path('list_type/', ListViewType.as_view(), name='list_types'),
    path('list_specialization/', ListViewSpecialization.as_view(), name='list_specializations'),
    path('list_specialist_schedules/', ListSpecialistSchedule.as_view(), name='list_specialist_schedules'),
    path('detail_specialist/<int:pk>/', DetailViewSpecialist.as_view(), name='detail_specialist'),
    path('list_specialist_appointments/',ListUserAppointment.as_view(), name='list_user_appointments')
]
