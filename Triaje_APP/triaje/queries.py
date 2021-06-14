from .models  import Usuario, Informe, DetalleInforme
from django.http import HttpResponse

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

def calcular_carga(dic_pat,dic_sint,usuario:Usuario):
    carga_total = 0
    edad = usuario.calcular_edad()

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

    res_imc = resultado_imc(usuario)
    if res_imc == "Delgadez severa":
        carga_total += 2
        if edad <= 12 or edad >= 80: 
            carga_total -= 1
    elif res_imc == "Delgadez moderada":
        carga_total += 1
    elif res_imc == "Sobrepeso":
        carga_total += 1
        if edad <= 16 or edad >= 50:
            carga_total += 1
    elif res_imc == "Obesidad":
        carga_total += 3
        if edad <= 16 or edad >= 50:
            carga_total += 1

    if edad >= 80:
        carga_total +=2
    elif edad >= 60:
        carga_total +=1 

    return carga_total

def determinar_gravedad(carga_total):
    if carga_total <= 10:
        return 'LEVE: Pida cita en su Centro de Salud.'
    elif carga_total <= 20:
        return 'MODERADO: Acuda de urgencia a su Centro de Salud.'
    else:
        print('Resultado = Grave')
        return 'GRAVE: Acuda de urgencia a un Hospital.'

def consulta_informe(username):
    dict_pat,dict_sint,usuario = informe(username)
    carga = calcular_carga(dict_pat,dict_sint,usuario)
    resultado = determinar_gravedad(carga)
    return resultado

def informe(username):
    usuario = Usuario.objects.get(username=username)
    informe = Informe.objects.filter(fk_usuario=usuario).last()
    dict_sin = sint_dict(informe)
    dict_pat = pat_dict(informe)

    return dict_pat,dict_sin,usuario

def sint_dict(informe):
    lista_sintoma= DetalleInforme.objects.filter(fk_informe=informe, fk_patologia=None)
    dic_sint = {}
    for item in lista_sintoma:
        dic_sint[ item.fk_sintoma.nombre ] = item.fk_sintoma
    return dic_sint

def pat_dict(informe):
    lista_patologia = DetalleInforme.objects.filter(fk_informe=informe, fk_sintoma=None)
    dict_pat = {}
    for item in lista_patologia:
        dict_pat[ item.fk_patologia.nombre ] = item.fk_patologia
    return dict_pat