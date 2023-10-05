from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Doctor,Appointment
from .serializers import DoctorSerializer,AppointmentSerializer
from typing import Final
from django.db.models import Q
from rest_framework import status
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

max_appointment: Final = 5
day : Final = {
    '0':'Monday',
    '1':'Tuesday',
    '2':'Wednesday',
    '3':'Thursday',
    '4':'Friday',
    '5':'Saturday',
    '6':'Sunday',
}


# Create your views here.
@api_view()
def doctor_api(request,pk=None):
    id=pk
    if id is not None:
        try:
            dc=Doctor.objects.get(pk=id)
            serializer=DoctorSerializer(dc)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            invalid_id={'message':'No doctor is listed with the given id'}
            return Response(invalid_id,status=status.HTTP_404_NOT_FOUND)
    dc=Doctor.objects.all()
    serializer=DoctorSerializer(dc,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def appointment_api(request):
    appointment_date=request.data.get('date')
    doctor=request.data.get('doctor')
    appointment_day=day[str(datetime.strptime(appointment_date,'%Y-%m-%d').weekday())]
    dc=Doctor.objects.get(pk=int(doctor))
    if dc is None or dc.weekly_schedule != appointment_day:
        invalid_date = {
            'message':'Doctor is not available on the given date'
        }
        return Response(invalid_date,status=status.HTTP_406_NOT_ACCEPTABLE)
    ap=Appointment.objects.filter(Q(doctor=doctor) & Q(date=appointment_date))
    if len(ap) < max_appointment:
        data=request.data
        serializer=AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            success_msg={
                "message":"Appointment scheduled on "+appointment_date
            }
            return Response(success_msg,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    limit_exceed = {
        'message': 'Appointment is full on '+ appointment_date
    }
    return Response(limit_exceed,status=status.HTTP_406_NOT_ACCEPTABLE);