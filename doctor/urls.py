from django.urls import path
from . import views
urlpatterns = [
    path('doctor/',views.doctor_api,name='doctor_list'),
    path('doctor/<int:pk>/',views.doctor_api,name='doctor_details'),
    path('appointment/',views.appointment_api,name='appointment'),
]
