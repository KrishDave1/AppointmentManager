from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Doctor, NewUser, Appointment
from .serializers import DoctorSerializer, NewUserSerializer, AppointmentSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
# from healthcare.helpers import send_otp_to_mobile
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def doctors(request):
    if request.method == 'GET':
        # speciality = request.query_params.get('speciality', None)
        doctor_Id = request.GET.get('id', None)
        specialization = request.GET.get('specialization', None)
        if doctor_Id is not None:
            doctors = NewUser.objects.filter(id=doctor_Id)
            if(not doctors.exists()):
                return Response({
                    'message' : 'User with this ID does not exist.'
                })
            if(doctors.first().type != NewUser.Types.DOCTOR):
                return Response({
                    'message' : 'User exists but is not of Doctor type.'
                })
            particular_Doctor = Doctor.objects.filter(id=doctor_Id).first()
            serializer = NewUserSerializer(doctors, many=True)
            # return Response(serializer.data)
            return Response({
                'about' : particular_Doctor.about,
                'specialization' : particular_Doctor.specialization,
                'is_Free' : particular_Doctor.is_Free,
                'doctor_As_NewUser' : serializer.data
            })
        elif specialization is not None:
            doctors = Doctor.objects.filter(specialization=specialization)
            doctors_Free = doctors.filter(is_Free=True)
            if(not doctors_Free.exists()):
                return Response({
                    'message': f"{specialization}s are not free right now."
                })
            serializer = DoctorSerializer(doctors_Free, many=True)
            return Response(serializer.data)
        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        try:
            serializer = DoctorSerializer(data=data)
            if not serializer.is_valid():
                # return Response(serializer.errors)
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'Doctor added to database, GET to check whether database was updated.',
                'id' : serializer.data['id']
            })
        except Exception as e:
            print(e)
            return Response({
                'status' : 200,
                'error' : 'something went wrong'
            })
    
    elif request.method == 'PUT':
        data = request.data
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Doctor.objects.get(id=data['id'])
        serializer = DoctorSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        try:
            obj = Doctor.objects.get(id=data['id'])
            name = obj.username
            obj.delete()
            return Response({'message' : f"{name} deleted successfully."})
        except Exception as e:
            return Response({'message' : f"Error is {e}"})
        
@api_view(["GET", "POST", "DELETE", "PATCH", "PUT"])
def appointments(request):
    if request.method == "GET":
        choice = request.GET.get('choice', None)
        if choice == "upcoming":
            appointments = Appointment.objects.filter(meeting_Date_Time__gt=timezone.now())
            if(not appointments.exists()):
                return Response({
                    'message' : 'Upcoming appointments do not exist.'
                })
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
        if choice == "past":
            appointments = Appointment.objects.filter(meeting_Date_Time__lt=timezone.now())
            if(not appointments.exists()):
                return Response({
                    'message' : 'Past appointments do not exist yet.'
                })
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
        if choice is None:
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
    elif request.method == "POST":
        data = request.data 
        serializer = AppointmentSerializer(data=data)
        try:
            if not serializer.is_valid():
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'Appointment added to database, GET to check the same.',
                'id' : serializer.data['id']
            })
        except Exception as e:
            return Response({
                'status' : 200,
                'message' : 'Something went wrong.'
            }) 
    elif request.method == "PUT":
        data = request.data 
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "PATCH":
        data = request.data 
        appointment = Appointment.objects.get(id=data['id'])
        serializer = AppointmentSerializer(appointment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "DELETE":
        data = request.data 
        try:
            appointment = Appointment.objects.get(id=data['id'])
            id = appointment.id 
            appointment.delete()
            return Response({
                'message' : f"Appointment {id} is successfully deleted."
            })
        except Exception as e:
            return Response({
                'message' : f"Error is {e}"
            })

def home(request):
    return HttpResponse('<h1>Hello</h1>')