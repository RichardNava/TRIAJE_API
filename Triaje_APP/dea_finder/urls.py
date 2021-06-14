from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("dea_list/", login_required(views.dea_list), name="dea_list"),
    path("dea_finder/", login_required(views.dea_finder), name="dea_finder"),
    path("dea_details/", login_required(views.details), name="dea_details"),
]