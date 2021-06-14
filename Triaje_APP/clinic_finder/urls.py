from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("clinic_list/", login_required(views.clinic_list), name="clinic_list"),
    path("clinic_finder/", login_required(views.clinic_finder), name="clinic_finder"),
    path("clinic_details/", login_required(views.clinic_details), name="clinic_details"),
]