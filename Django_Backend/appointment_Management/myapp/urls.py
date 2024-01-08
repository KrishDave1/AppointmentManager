from django.urls import path
from myapp import views

urlpatterns = [
    path('', view=views.home),
    path('appointments/', view=views.appointments),
    path('doctors/', view=views.doctors)
]
