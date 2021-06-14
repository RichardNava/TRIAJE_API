from django.shortcuts import redirect, render
from .models import DEA
from .queries import *

def dea_list(request):
    deas = DEA.objects.all()
    context = {"deas": deas}
    return render(request, "finder/dea_list.html", context)
    
def dea_finder(request):
    if request.method == "POST":
        lat = (request.POST['lat'])
        lng =  (request.POST['lng'])
        range_dea = request.POST['range_dea']
        deas = DEA.objects.all()
        top_near_deas = near_dea_order(float(lat), float(lng), deas)
        urls, deas = dea_links_maps(top_near_deas, float(lat), float(lng), int(range_dea))    
        for_range = list(range(int(range_dea)))
        context = {"deas": deas, "urls": urls, "range_dea": range_dea, "for_range": for_range}
        return render(request, "finder/dea_finder.html", context)
    else:
        return render(request, "finder/user_dea.html")
        
def details(request):
    if request.method == "POST":
        lat = (request.POST['lat'])
        lng =  (request.POST['lng'])
        codigo_dea = request.POST["codigo_dea"]
        dea = DEA.objects.filter(codigo_dea=codigo_dea)[0]
        distance = distance_dea(dea=dea,user_lat=lat,user_lng=lng)
        dea_latlong = utm.to_latlon(dea.x_utm, dea.y_utm,30,"T")
        url = f"https://www.google.com/maps/search/?api=1&query={dea_latlong[0]},{dea_latlong[1]}"
        context = {"dea": dea, "url":url, "distance": round(distance)}
        return render(request, "finder/dea_details.html", context)
    else:
        return redirect("/dea_list")

# def user(request):
#     return render(request, "finder/user.html")


# def dea_finder(request):
#     if request.method == "POST":
#         lat = (request.POST['lat'])
#         lng =  (request.POST['lng'])
#         deas = DEA.objects.all()
#         dea, url = nearest_dea(float(lat), float(lng), deas)
#         context = {"dea": dea, "url": url}
#         return render(request, "finder/dea_finder.html", context)
#     else:
#         return render(request, "finder/user.html")