from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import (login as auth_login, authenticate)
from .models import Paciente, Sintoma, Patologia, DetalleInforme, Informe
import csv
import os

di_path = os.path.realpath(__file__)[0:-8]
hepatitis_list = ['HEPATITIS A, HEPATITIS B, HEPATITIS C, HEPATITIS D, HEPATITIS E']
lipo_list = ['HIPERCOLESTEROLEMIA','HIPERTRIGLICERIDEMIA']

def calcular_imc(peso,altura):
    altura_imc = altura/100
    imc = peso/(altura_imc**2)
    return imc

def resultado_imc(paciente):
    imc = calcular_imc(paciente.peso,paciente.altura)
    if (imc < 16):
        return "Delgadez severa"
    elif (imc < 16.99):
        return "Delgadez moderada"
    elif (imc < 18.49):
        return "Delgadez aceptable"
    elif (imc < 24.99):
        return "Peso normal"
    elif (imc < 29.99):
        return "Sobrepeso"
    elif (imc < 34.99):
        return "Obesidad"

def calcular_carga(dic_pat,dic_sint,paciente:Paciente):
    carga_total = 0

    for key_sint, obj_sint in dic_sint.items():
        carga_total += obj_sint.grado
        for key_pat in dic_pat.keys():
            if key_sint.upper() == 'DIFICULTAD RESPIRATORIA': 
                if key_pat.upper() == 'ASMA':
                    carga_total += 5
                elif  key_pat.upper() == 'OTRAS ALERGIAS':
                    carga_total += 3
                elif  key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 3
                elif  key_pat.upper() == 'ALERGIAS A POLENES':
                    carga_total += 4
                elif  key_pat.upper() == 'APNEA DEL SUEÑO':
                    carga_total += 2                    
                elif  key_pat.upper() == 'TUBERCULOSIS':
                    carga_total += 10
            if key_sint.upper() == 'DISNEA' or key_sint.upper() == 'APNEA': 
                if key_pat.upper() == 'ASMA':
                    carga_total += 3
                elif  key_pat.upper() == 'OTRAS ALERGIAS':
                    carga_total += 2
                elif  key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 2
                elif  key_pat.upper() == 'ALERGIAS A POLENES':
                    carga_total += 2
                elif  key_pat.upper() == 'APNEA DEL SUEÑO':
                    carga_total += 3                    
                elif  key_pat.upper() == 'TUBERCULOSIS':
                    carga_total += 3
            if key_sint.upper() == 'FIEBRE ALTA' or key_sint.upper() == 'FIEBRE MEDIA': 
                if key_pat.upper() in hepatitis_list:
                    carga_total += 10
                elif  key_pat.upper() == 'OTRAS ALERGIAS':
                    carga_total += 4
                elif  key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 5
                elif  key_pat.upper() == 'SIDA':
                    carga_total += 10
                elif  key_pat.upper() == 'TRANSPLANTE PREVIO RECIENTE':
                    carga_total += 10                    
                elif  key_pat.upper() == 'TUBERCULOSIS':
                    carga_total += 10
                elif  key_pat.upper() == 'CISTITIS RECURRENTE' or key_pat.upper() == 'CANDIDIASIS RECURRENTE':
                    carga_total += 3
            if key_sint.upper() == 'DOLOR ABDOMINAL': 
                if key_pat.upper() in hepatitis_list:
                    carga_total += 10
                elif key_pat.upper() == 'INSUFICIENCIA RENAL':
                    carga_total += 8
                elif key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 6
                elif key_pat.upper() == 'INTOLERANCIAS':
                    carga_total += 6
                elif key_pat.upper() == 'ENFERMEDAD DE CROHN':
                    carga_total += 10                    
                elif key_pat.upper() in lipo_list:
                    carga_total += 2
            if key_sint.upper() == 'PALPITACIONES': 
                if key_pat.upper() == 'PROBLEMAS DE COAGULACION':
                    carga_total += 5
                elif key_pat.upper() == 'INSUFICIENCIA CARDIACA':
                    carga_total += 20
            if key_sint.upper() == 'VERTIGOS' and key_pat.upper() == 'VERTIGOS':
                carga_total += 20

    for key_pat, obj_pat in dic_pat.items():
        carga_total += obj_pat.grado

    res_imc = resultado_imc(paciente)
    if res_imc == "Delgadez severa":
        carga_total += 2
        if paciente.edad <= 12 or paciente.edad >= 80: 
            carga_total -= 1
    elif res_imc == "Delgadez moderada":
        carga_total += 1
    elif res_imc == "Sobrepeso":
        carga_total += 1
        if paciente.edad <= 16 or paciente.edad >= 50:
            carga_total += 1
    elif res_imc == "Obesidad":
        carga_total += 3
        if paciente.edad <= 16 or paciente.edad >= 50:
            carga_total += 1

    if paciente.edad >= 80:
        carga_total +=2
    elif paciente.edad >= 60:
        carga_total +=1 

    return carga_total

def create_sintoma(nombre,grado,valor_adicional):
    obj = Sintoma.create(nombre,grado,valor_adicional)
    return HttpResponse(obj)

def create_paciente(dni,edad,peso,altura):
    obj = Paciente.create(dni,edad,peso,altura)
    return HttpResponse(obj)

def create_patologia(nombre,grado,valor_adicional):
    obj = Patologia.create(nombre,grado,valor_adicional)
    return HttpResponse(obj)

def determinar_gravedad(carga_total):
    if carga_total <= 10:
        print('Resultado = Leve')
        return 'LEVE: Pida cita en su Centro de Salud.'
    elif carga_total <= 20:
        print('Resultado = Moderado')
        return 'MODERADO: Acuda de urgencia a su Centro de Salud.'
    else:
        print('Resultado = Grave')
        return 'GRAVE: Acuda de urgencia a un Hospital.'

def consulta_informe(dni):
    lista_patologia,lista_sintoma,paciente = informe(dni)
    carga = calcular_carga(lista_patologia,lista_sintoma,paciente)
    resultado = determinar_gravedad(carga)
    return resultado

def informe(dni):
    paciente = Paciente.objects.get(dni=dni)
    informe = Informe.objects.filter(fk_paciente=paciente).last()
    lista_sintoma= DetalleInforme.objects.filter(fk_informe=informe, fk_patologia=None)
    lista_patologia = DetalleInforme.objects.filter(fk_informe=informe, fk_sintoma=None)

    dic_sin = {}
    for item in lista_sintoma:
        dic_sin[ item.fk_sintoma.nombre ] = item.fk_sintoma

    dic_pat = {}
    for item in lista_patologia:
        dic_pat [ item.fk_patologia.nombre ] = item.fk_patologia

    return dic_pat,dic_sin,paciente

def datos_paciente(request):
    msg = 'Introduzca sus datos'
    if request.method == 'POST':
        # if Paciente.objects.get(dni=request.POST['dni']) is not None:
        paciente = Paciente.create(request.POST['dni'],request.POST['edad'],request.POST['peso'],request.POST['altura'])
        Informe.objects.create(fk_paciente=paciente)
        patologias = Patologia.objects.all()
        patologias1 = patologias[0:11]
        patologias2 = patologias[11:22]
        patologias3 = patologias[22:33]
        context = {'paciente': paciente, 'patologias1': patologias1, 'patologias2': patologias2, 'patologias3': patologias3}
        return render(request,'triaje/patologias.html', context)
        # else:
        #     msg = 'El paciente ya existe'

    context = {'message': msg}
    return render(request,'triaje/datosPaciente.html', context)

def patologias_form(request):
    msg = 'PRUEBA'
    if request.method == 'POST':
        patologias = Patologia.objects.all()
        sintomas = Sintoma.objects.all()
        sintomas1 = sintomas[0:14]
        sintomas2 = sintomas[14:28]      
        sintomas3 = sintomas[28:]      
        paciente = Paciente.objects.get(dni=request.POST['dni'])
        informe = Informe.objects.filter(fk_paciente=paciente).last()      
        for pat in patologias:
            if request.POST.get(pat.nombre):
                patologia = Patologia.objects.get(id=request.POST[pat.nombre])
                DetalleInforme.objects.create(fk_informe=informe, fk_patologia = patologia, fk_sintoma=None)
        context = {'paciente': paciente, 'sintomas1': sintomas1, 'sintomas2': sintomas2, 'sintomas3': sintomas3}
        return render(request,'triaje/sintomas.html', context)
    context = {'message': msg}
    return render(request,'triaje/patologias.html', context)

def sintomas_form(request):
    msg = 'PRUEBA'
    if request.method == 'POST':
        sintomas = Sintoma.objects.all()
        paciente = Paciente.objects.get(dni=request.POST['dni'])
        informe = Informe.objects.filter(fk_paciente=paciente).last()      
        for sint in sintomas:
            if request.POST.get(sint.nombre):
                sintoma = Sintoma.objects.get(id=request.POST[sint.nombre])
                DetalleInforme.objects.create(fk_informe=informe, fk_patologia = None, fk_sintoma=sintoma)
        resultado = consulta_informe(request.POST['dni'])
        context = {'resultado': resultado}
        return render(request,'triaje/resultado.html', context)
    context = {'message': msg}
    return render(request,'triaje/sintomas.html', context)

def load_sint_csv():
    file_csv = open(f'{di_path}sintomas.csv', 'r',encoding='utf8')
    read = csv.reader(file_csv)
    sint_resp = ''
    lista_sintoma = Sintoma.objects.all()
    dic_sin = {}
    for item in lista_sintoma:
        dic_sin[ item.nombre ] = item
    for row in read:
        if not row[0].upper() in dic_sin.keys():
            obj = Sintoma.create(row[0].upper(),row[1],row[2])
            sint_resp += obj.toStr() + '<br>'
        else:
            sint_resp += 'El sintoma '+row[0].upper()+' ya existe en la base de datos. <br>'
    file_csv.close()
    return HttpResponse(sint_resp)

def load_pat_csv():
    file_csv = open(f'{di_path}patologias.csv', 'r',encoding='utf8')
    read = csv.reader(file_csv)
    pat_resp = ''
    lista_patologia = Patologia.objects.all()
    dic_pat = {}
    for item in lista_patologia:
        dic_pat[ item.nombre ] = item
    for row in read:
        if not row[0].upper() in dic_pat.keys():
            obj = Patologia.create(row[0].upper(),row[1],row[2])
            pat_resp += obj.toStr() + '<br>'
        else:
            pat_resp += 'La Patologia '+row[0].upper()+' ya existe en la base de datos. <br>'
    file_csv.close()
    return HttpResponse(pat_resp)
