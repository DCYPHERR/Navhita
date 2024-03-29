# Generated by Django 4.1.5 on 2023-03-27 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_patient_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareTaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='caretaker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='caretaker',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient', to='app.caretaker'),
        ),
    ]
