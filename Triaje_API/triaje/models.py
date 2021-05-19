from django.db import models
from datetime import datetime

class Paciente(models.Model):
    dni = models.CharField(max_length=9,blank=True)
    edad = models.IntegerField(default=0)
    peso = models.FloatField(default=0.0)
    altura = models.IntegerField(default=0) # Expresada en centimetros

    def __str__(self):
        return f'PACIENTE - DNI: {self.dni}, Edad: {self.edad}, Peso: {self.peso}, Altura: {self.altura}'

    def toStr(self):
        return Paciente.__str__(self)

    def create(dni,edad,peso,altura):
        obj = Paciente.objects.create(dni = dni, edad = edad, peso = peso, altura = altura)
        return obj

class Sintoma(models.Model):
    nombre = models.CharField(max_length=50)
    grado = models.IntegerField(default=0)
    dato_adicional = models.CharField(max_length=50,blank=True)

    def __str__(self):
        cadena = f'{self.id} - {self.nombre.upper()} {self.dato_adicional} '
        return cadena

    def toStr(self):
        return Sintoma.__str__(self)

    def create(nombre,grado,dato_adicional):
        obj = Sintoma.objects.create(nombre = nombre.upper(), grado = grado, dato_adicional=dato_adicional)
        return obj

class Patologia(models.Model):
    nombre = models.CharField(max_length=50)
    grado = models.IntegerField(default=0)
    dato_adicional = models.CharField(max_length=50,blank=True)

    def __str__(self):
        cadena = f'{self.id} - {self.nombre.upper()} {self.dato_adicional} '
        return cadena

    def toStr(self):
        return Patologia.__str__(self)

    def create(nombre,grado,dato_adicional):
        obj = Patologia.objects.create(nombre = nombre, grado = grado,dato_adicional=dato_adicional)
        return obj

class Informe(models.Model):
    fk_paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=datetime.now())

    def __str__(self):
        cadena = f'{self.id} - {self.nombre.upper()} '
        if dato_adicional != '':
            cadena += dato_adicional
        return cadena

    def __str__(self):
        return f'{self.fk_paciente}, Fecha:{self.fecha}'


class DetalleInforme(models.Model):
    fk_sintoma = models.ForeignKey(Sintoma,on_delete=models.CASCADE,null=True,blank=True)
    fk_patologia = models.ForeignKey(Patologia,on_delete=models.CASCADE, null=True,blank=True)
    fk_informe = models.ForeignKey(Informe,on_delete=models.CASCADE)

    def __str__(self):
        cadena  = ''
        if self.fk_patologia == None:
            cadena = f'{self.fk_informe} <br> {self.fk_sintoma} '
        else:
            cadena = f'{self.fk_informe} <br> {self.fk_patologia} '
        return cadena
    
    def create_sintoma(fk_informe,fk_sintoma):
        obj = DetalleInforme.objects.create(fk_informe=fk_informe,fk_sintoma=fk_sintoma)

    def create_patologia(fk_informe,fk_patologia):
        obj = DetalleInforme.objects.create(fk_informe=fk_informe,fk_sintoma=fk_patologia)
