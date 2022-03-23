# Generated by Django 3.0.6 on 2022-03-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0004_auto_20220320_2020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='a_from',
            new_name='a_time',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='a_to',
        ),
        migrations.AddField(
            model_name='appointment',
            name='a_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]