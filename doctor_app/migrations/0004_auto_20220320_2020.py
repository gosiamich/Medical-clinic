# Generated by Django 3.0.6 on 2022-03-20 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0003_auto_20220320_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='clinic',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Clinic'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='a_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
