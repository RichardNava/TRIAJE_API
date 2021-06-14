import csv
import os
from django.views.generic.edit import FormView
from .forms import FormularioUsuario, FormularioLogin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout 
from .models import Sintoma, Patologia, DetalleInforme, Informe, Usuario
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .queries import *

di_path = os.path.realpath(__file__)[0:-8]

def user_list(request):
    user_list = Usuario.objects.all()
    context= {'user_list': user_list}
    return render(request,'triaje/user_list.html',context)

def user_details(request):
    if request.method == 'POST':
        id_usuario = request.POST['user_id']
        usuario = Usuario.objects.filter(id=id_usuario)[0]
        print(usuario.username)
        context = {'usuario': usuario}
        return render(request,'triaje/user_details.html', context)

def user_delete(request,id):
    usuario = Usuario.objects.get(id=id)
    context = {'usuario': usuario}
    if request.method == 'POST':
        Usuario.objects.filter(id=request.POST['user_id']).delete()
        return redirect('user_list')
    return render(request,'triaje/user_delete.html/', context)

def delete_informe(request,id):
    info = Informe.objects.get(id=id)
    context = {'informe': info}
    if request.method == 'POST':
        Informe.objects.filter(id=request.POST['id_del']).delete()
        return redirect('informe_list')
    return render(request,'triaje/info_delete.html/', context)

def info_details(request):
    if request.method == 'POST':
        id_informe = request.POST['id_info']
        info_detail = DetalleInforme.objects.filter(fk_informe=id_informe)
        dict_sin = sint_dict(id_informe)
        dict_pat = pat_dict(id_informe)
        carga = calcular_carga(dict_pat, dict_sin, request.user)
        resultado = determinar_gravedad(carga)
        context = {'details': info_detail, 'id_informe': id_informe, 'resultado': resultado}
        return render(request,'triaje/info_details.html', context)

def info_list(request):
    informes = Informe.objects.filter(fk_usuario=request.user.id)
    context = {"informes": informes}
    return render(request,'triaje/info_list.html', context)

def datos_paciente(request):
    usuario = Usuario.objects.get(username=request.user.username)
    Informe.objects.create(fk_usuario=usuario)
    patologias = Patologia.objects.all()
    patologias1 = patologias[0:11]
    patologias2 = patologias[11:22]
    patologias3 = patologias[22:33]
    context = {'usuario': usuario, 'patologias1': patologias1, 'patologias2': patologias2, 'patologias3': patologias3}
    return render(request,'triaje/patologias.html', context)

def patologias_form(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(username=request.user.username)
        informe = Informe.objects.filter(fk_usuario=usuario).last()      
        patologias = Patologia.objects.all()
        sintomas = Sintoma.objects.all()
        sintomas1 = sintomas[0:14]
        sintomas2 = sintomas[14:28]      
        sintomas3 = sintomas[28:]      
        for pat in patologias:
            if request.POST.get(pat.nombre):
                patologia = Patologia.objects.get(id=request.POST[pat.nombre])
                DetalleInforme.objects.create(fk_informe=informe, fk_patologia = patologia, fk_sintoma=None)
        context = {'usuario': usuario, 'sintomas1': sintomas1, 'sintomas2': sintomas2, 'sintomas3': sintomas3}
        return render(request,'triaje/sintomas.html', context)
    return render(request,'triaje/patologias.html')

def sintomas_form(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(username=request.user.username)
        sintomas = Sintoma.objects.all()
        informe = Informe.objects.filter(fk_usuario=usuario).last()      
        for sint in sintomas:
            if request.POST.get(sint.nombre):
                sintoma = Sintoma.objects.get(id=request.POST[sint.nombre])
                DetalleInforme.objects.create(fk_informe=informe, fk_patologia = None, fk_sintoma=sintoma)
        resultado = consulta_informe(request.user.username)
        context = {'resultado': resultado}
        return render(request,'triaje/resultado.html', context)
    return render(request,'triaje/sintomas.html')


def load_sint_csv(request):
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

def load_pat_csv(request):
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

def logout_usuario(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
    if request.user.is_authenticated:
        return render(request, 'triaje/index.html')

class ListadoUsuario(ListView):
    model = Usuario
    template_name = 'triaje/listado_usuarios.html'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo= True)

class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'triaje/crear_usuario.html'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = Usuario(
                username = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),
                fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento'),
                peso = form.cleaned_data.get('peso'),
                altura = form.cleaned_data.get('altura')
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            return redirect('listado_usuarios')
        else:
            return render(request,self.template_name,{'form':form})

class Login(FormView):
    template_name = 'triaje/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
