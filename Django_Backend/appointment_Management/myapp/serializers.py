from rest_framework import serializers
from .models import NewUser, Doctor, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = [
            # "password",
            "type",
            "is_staff",
            # "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            # "is_superuser",
            # "id"
        ]
        depth = 1

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        exclude = [
            # "password",
            "is_staff",
            # "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            # "is_superuser",
            # "id"
        ]
        depth = 1

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1