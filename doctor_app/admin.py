from django.contrib import admin

# Register your models here.
from .models import Patient, Specialist, Appointment, Schedule, Address, Clinic, Specialization, Type

admin.site.register(Patient)
admin.site.register(Specialist)
admin.site.register(Appointment)
admin.site.register(Schedule)
admin.site.register(Address)
admin.site.register(Clinic)
admin.site.register(Specialization)
admin.site.register(Type)