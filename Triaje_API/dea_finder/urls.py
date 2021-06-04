from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("listado/", login_required(views.listado), name="listado"),
    path("finder/", login_required(views.dea_finder), name="finder"),
    path("details/", login_required(views.details), name="details"),
]