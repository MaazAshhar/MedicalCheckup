from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Doctor(models.Model):
    name=models.CharField(max_length=80)
    specialization=models.CharField(max_length=100)
    weekly_schedule=models.CharField(max_length=80)
    doctor_details=models.TextField()
    location=models.CharField(max_length=100)


class Appointment(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=100)
    address=models.TextField()
    age=models.IntegerField()
    mobile=models.CharField(max_length=10)
    date=models.DateField()