from django.db import models

class DEA(models.Model):
    codigo_dea = models.CharField(max_length=100) 
    direccion_ubicacion = models.CharField(max_length=100) 
    direccion_via_nombre = models.CharField(max_length=100) 
    direccion_portal_numero = models.CharField(max_length=100)
    horario_acceso = models.CharField(max_length=100)
    x_utm = models.IntegerField(default=None)
    y_utm = models.IntegerField(default=None)