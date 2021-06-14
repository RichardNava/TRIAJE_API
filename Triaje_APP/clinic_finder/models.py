from django.db import models

class Hospital(models.Model):
    nro_registro = models.CharField(max_length=7)
    direccion_ubicacion = models.CharField(max_length=100) 
    direccion_vial_numero = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=100)
    dependecia = models.CharField(max_length=100)
    x_utm = models.IntegerField(default=None)
    y_utm = models.IntegerField(default=None)