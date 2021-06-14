from django.shortcuts import redirect, render
from .models import Hospital
from .queries import *

def clinic_list(request):
    hospitals = Hospital.objects.all()
    context = {"hospitals": hospitals}
    return render(request, "clinic_finder/clinic_list.html", context)

def clinic_finder(request):
    if request.method == "POST":
        lat = (request.POST['lati'])
        lng = (request.POST['long'])
        range_hosp = request.POST['range_hosp']
        hospitals = Hospital.objects.all()
        top_near_clinics = near_clinic_order(float(lat), float(lng), hospitals)
        urls, hospitals = clinic_links_maps(top_near_clinics, float(lat), float(lng), int(range_hosp))  
        for_range = list(range(int(range_hosp)))      
        context = {"hospitals": hospitals, "urls": urls, "range_hosp": range_hosp, "for_range": for_range}
        return render(request, "clinic_finder/clinic_finder.html", context)
    else:
        return render(request, "clinic_finder/user_clinic.html")

def clinic_details(request):
    if request.method == "POST":
        lat = (request.POST['lati'])
        lng =  (request.POST['long'])
        nro_registro = request.POST["nro_registro"]
        hospital = Hospital.objects.filter(nro_registro=nro_registro)[0]
        distance = distance_clinic(hospital=hospital,user_lat=lat,user_lng=lng)
        hosp_latlong = utm.to_latlon(hospital.x_utm, hospital.y_utm,30,"T")
        url = f"https://www.google.com/maps/search/?api=1&query={hosp_latlong[0]},{hosp_latlong[1]}"
        context = {"hospital": hospital, "url":url, "distance": round(distance)}
        return render(request, "clinic_finder/clinic_details.html", context)
    else:
        return redirect("/clinic_list")