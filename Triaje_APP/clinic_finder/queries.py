import os
import json
import utm
from .models import Hospital

di_path = os.path.realpath(__file__)[0:-10]

# import requests as req #? Importar la BBDD 

# response = req.get("https://datos.comunidad.madrid/catalogo/dataset/a48d63fd-91ce-4b37-8fff-36a8dcad293e/resource/bb4a0a8e-4d4d-4548-a651-1b8fc0990ca5/download/centros_servicios_establecimientos_sanitarios.json").json()

# with open (f"{di_path}hospitals.json","w", encoding='utf8') as file:
#     json.dump(response, file, ensure_ascii=False, indent=4)

# with open (f"{di_path}clinics.json","w", encoding='utf8') as file:
#     json.dump(response, file, ensure_ascii=False, indent=4)

def get_data():
    with open(f"{di_path}clinics.json", encoding="utf8") as file:
        return json.load(file)

def insert_hospital(dataset):
    no_repeat = []
    for hospital in dataset:
        if hospital["centro_tipo"].find("Hospital") != -1 and hospital["centro_nro_registro"] not in no_repeat:
            no_repeat.append(hospital["centro_nro_registro"])
            nro_registro = hospital["centro_nro_registro"]
            direccion_ubicacion = hospital["direccion_vial_nombre"]
            direccion_vial_numero = hospital["direccion_vial_nro"]
            codigo_postal = hospital["direccion_codigo_postal"]
            dependencia = hospital["dependecia_patrimonial"]
            x_utm = hospital["localizacion_coordenada_x"]
            y_utm = hospital["localizacion_coordenada_y"]

            Hospital.objects.create(
                nro_registro = nro_registro,
                direccion_ubicacion = direccion_ubicacion,
                direccion_vial_numero = direccion_vial_numero,
                codigo_postal = codigo_postal,
                dependecia = dependencia,
                x_utm = x_utm,
                y_utm = y_utm
            )

class Clinic:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def calculate_distance(self, user_x, user_y):
        result = ((user_x - self.pos_x)**2 + (user_y - self.pos_y)**2)**0.5
        return result

def near_clinic_order(user_lat, user_long, dataset):
    user_xy = utm.from_latlon(user_lat, user_long)
    hospital_dict = {}
    for hosp in dataset:
        new_clinic = Clinic(hosp.x_utm, hosp.y_utm)
        distance = new_clinic.calculate_distance(user_xy[0], user_xy[1])
        hospital_dict[(hosp.x_utm, hosp.y_utm)] = distance
    return dict(sorted(hospital_dict.items(), key=lambda item: item[1]))

def clinic_links_maps(hospital_dict, user_lat, user_long, range=5):
    hospitals_urls = []
    hospitals_data = []
    for hosp in list(hospital_dict.keys())[0:int(range)]:
        latlong = utm.to_latlon(int(hosp[0]),int(hosp[1]),30,'T')
        hospitals_data.append(Hospital.objects.filter(x_utm= int(hosp[0]), y_utm= int(hosp[1]))[0])
        hospitals_urls.append(f'https://www.google.com/maps/dir/{user_lat},{user_long}/{latlong[0]},{latlong[1]}')
    return hospitals_urls,hospitals_data

def distance_clinic(hospital,user_lat,user_lng):
    new_hosp= Clinic(hospital.x_utm, hospital.y_utm)
    user_xy = utm.from_latlon(float(user_lat), float(user_lng))
    distance = new_hosp.calculate_distance(user_xy[0], user_xy[1])
    return distance

