from django.contrib import admin
from .models import Doctor, Appointment
# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display=['id','name','specialization','weekly_schedule']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=['doctor','patient_name','address','age','mobile','date']