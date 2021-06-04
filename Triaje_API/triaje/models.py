from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,fecha_nacimiento,peso,altura,password= None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')

        usuario = self.model(
            username=username,
            fecha_nacimiento=fecha_nacimiento,
            peso=peso,
            altura=altura, 
            email= self.normalize_email(email)
            )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self,username,fecha_nacimiento,peso,altura,email,password):
        usuario = self.create_user(
            email,
            username=username,
            fecha_nacimiento=fecha_nacimiento,
            peso=peso,
            altura=altura, 
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique = True, max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    peso = models.FloatField('Peso', default=0.0)
    altura = models.IntegerField('Altura en cm', default=0)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','fecha_nacimiento','peso','altura']

    def __str__(self):
        return f'{self.username}'

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
    
    def calcular_edad(self):
        return datetime.today().year - self.fecha_nacimiento.year 

    @property
    def is_staff(self):
        return self.usuario_administrador

class Informe(models.Model):
    fk_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=datetime.now())

    # def __str__(self):
    #     cadena = f'{self.id} - {self.nombre.upper()} '
    #     if Patologia.dato_adicional != '':
    #         cadena += Patologia.dato_adicional
    #     elif Sintoma.dato_adicional != '':
    #         cadena += Sintoma.dato_adicional
    #     return cadena

    def __str__(self):
        return f'{self.fk_usuario}, Fecha:{self.fecha}'

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
        DetalleInforme.objects.create(fk_informe=fk_informe,fk_sintoma=fk_sintoma)

    def create_patologia(fk_informe,fk_patologia):
        DetalleInforme.objects.create(fk_informe=fk_informe,fk_sintoma=fk_patologia)