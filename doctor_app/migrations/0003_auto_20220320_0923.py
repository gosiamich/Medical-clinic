# Generated by Django 3.0.6 on 2022-03-20 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0002_auto_20220320_0921'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together={('specialist', 'v_date', 'time_slot')},
        ),
    ]
