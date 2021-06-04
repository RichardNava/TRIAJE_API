import os
import json
import utm
from .models  import DEA

di_path = os.path.realpath(__file__)[0:-10]

def get_data():
    with open(f"{di_path}deas.json", encoding="utf8") as file:
        return json.load(file)

data = get_data()["data"]

def insert_into(dataset):
    for dea in dataset:
        codigo_dea = dea["codigo_dea"]
        direccion_ubicacion = dea["direccion_ubicacion"]
        direccion_via_nombre = dea["direccion_via_nombre"]
        direccion_portal_numero = dea["direccion_portal_numero"]
        horario_acceso = dea["horario_acceso"]
        x_utm = dea["direccion_coordenada_x"]
        y_utm = dea["direccion_coordenada_y"]

        DEA.objects.create(
            codigo_dea = codigo_dea,
            direccion_ubicacion = direccion_ubicacion,
            direccion_via_nombre = direccion_via_nombre,
            direccion_portal_numero = direccion_portal_numero,
            horario_acceso = horario_acceso,
            x_utm = x_utm,
            y_utm = y_utm
        )

class Dea:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def calculate_distance(self, user_x, user_y):
        result = ((user_x - self.pos_x)**2 + (user_y - self.pos_y)**2)**0.5
        return result

def nearest_dea(user_lat, user_long, dataset):
    user_xy = utm.from_latlon(user_lat, user_long)
    first_dea = list(dataset)[0]
    result = first_dea
    first_object = Dea(first_dea.x_utm, first_dea.y_utm)
    distance_to_beat = first_object.calculate_distance(user_xy[0], user_xy[1])

    for dea in dataset:
        dea_object = Dea(dea.x_utm, dea.y_utm)
        distance = dea_object.calculate_distance(user_xy[0], user_xy[1])
        if distance <= distance_to_beat:
            result = dea
            distance_to_beat = distance
        else:
            continue

    dea_latlng = utm.to_latlon(result.x_utm,result.y_utm, 30, "N")
    url = f"https://www.google.com/maps/dir/{user_lat},{user_long}/{dea_latlng[0]},{dea_latlng[1]} "
    return result, url

def distance_dea(dea,user_lat,user_lng):
    new_dea = Dea(dea.x_utm, dea.y_utm)
    user_xy = utm.from_latlon(float(user_lat), float(user_lng))
    distance = new_dea.calculate_distance(user_xy[0], user_xy[1])
    return distance

def near_dea_order(user_lat, user_long, dataset):
    user_xy = utm.from_latlon(user_lat, user_long)
    dea_dict = {}
    for dea in dataset:
        new_dea = Dea(dea.x_utm, dea.y_utm)
        distance = new_dea.calculate_distance(user_xy[0], user_xy[1])
        dea_dict[(dea.x_utm, dea.y_utm)] = distance
    return dict(sorted(dea_dict.items(), key=lambda item: item[1]))

def dea_links_maps(dea_dict, user_lat, user_long, range=5):
    deas_urls = []
    deas_data = []
    for dea in list(dea_dict.keys())[0:int(range)]:
        latlong = utm.to_latlon(int(dea[0]),int(dea[1]),30,'T')
        # pos_me = utm.to_latlon(user_lat,user_long,30,'T')
        deas_data.append(DEA.objects.filter(x_utm= int(dea[0]), y_utm= int(dea[1]))[0])
        deas_urls.append(f'https://www.google.com/maps/dir/{user_lat},{user_long}/{latlong[0]},{latlong[1]}')
    return deas_urls,deas_data