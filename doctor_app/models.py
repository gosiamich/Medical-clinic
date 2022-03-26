from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


gender_choice = (
    ("F", "Female"),
    ("M", "Male"),
)


class Specialization(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Address(models.Model):
    city = models.CharField(max_length=128)
    postcode = models.CharField(max_length=6)
    street = models.CharField(max_length=128)
    building_number = models.CharField(max_length=50)

    def __str__(self):
        return f'ul. {self.street} {self.building_number}, {self.city} ({self.postcode})'


class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    pesel = models.CharField(max_length=11,unique=True)
    gender = models.CharField(max_length=55, choices=gender_choice)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse('detail_patient', args=(self.id,))


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    phone_number = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse('detail_specialist', args=(self.id,))


    def set_clinic(self):
        return set(self.clinic_set.all())


class Clinic(models.Model):
    name = models.CharField(max_length=128)
    phone_number = models.PositiveIntegerField()
    email = models.CharField(max_length=128, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    specialists = models.ManyToManyField(Specialist,  through="Schedule")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('detail_clinic', args=(self.id,))

    def get_update_url(self):
        return f'/modify_clinic/{self.id}/'

    def set_spec(self):
        return set(self.specialists.all())


WEEK_DAY = (
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
)


class Schedule(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=WEEK_DAY)
    sch_from = models.TimeField(verbose_name='Time from')
    sch_to = models.TimeField(verbose_name='Time to')

    def get_update_url(self):
        return f'/update_schedule/{self.id}/'

    def get_delete_url(self):
        return f'/delete_schedule/{self.id}/'

    class Meta:
        unique_together = ['specialist', 'clinic', 'day_of_week']


class Type(models.Model):
    name = models. CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    a_date = models.DateField()
    a_time = models.TimeField()
    a_date_time = models.DateTimeField(null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def weekday_from_date(self):
        return self.a_date.isoweekday()

    def get_delete_url(self):
        return f'/delete_appointment/{self.id}/'

    class Meta:
        unique_together = ['specialist', 'a_date', 'a_time', 'clinic']



TIME_SLOT = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
        (8, '17:00 – 17:30'),
    )


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    v_date = models.DateField()
    time_slot = models.IntegerField(choices=TIME_SLOT)


    class Meta:
        unique_together = ['specialist', 'v_date', 'time_slot']


