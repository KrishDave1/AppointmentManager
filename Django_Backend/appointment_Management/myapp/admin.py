from django.contrib import admin
from myapp.models import Appointment, Doctor

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Doctor)