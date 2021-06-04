from django.urls import path
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('listado_usuarios/', login_required(views.ListadoUsuario.as_view()), name='listado_usuarios'),
    path('crear_usuario/', views.RegistrarUsuario.as_view(), name='crear_usuario'),
    path('consulta_informe/<str:dni>', views.consulta_informe, name='consulta_informe'),
    path('load_sint_csv/', views.load_sint_csv, name='load_sint_csv'),
    path('load_pat_csv/', views.load_pat_csv, name='load_pat_csv'),
    path('datos_paciente/', login_required(views.datos_paciente), name='datos_paciente'),
    path('patologias/', login_required(views.patologias_form), name='patologias'),
    path('sintomas/', login_required(views.sintomas_form), name='sintomas'),
    #path('', LoginView.as_view(template_name='triaje/login.html'), name='login'),
    path('', views.Login.as_view(), name='login'),
    # path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(views.logout_usuario), name='logout'),
    path('index/', views.index, name='index'),
]