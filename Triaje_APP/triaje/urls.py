from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('listado_usuarios/', login_required(views.ListadoUsuario.as_view()), name='listado_usuarios'),
    path('crear_usuario/', views.RegistrarUsuario.as_view(), name='crear_usuario'),
    path('consulta_informe/', login_required(views.consulta_informe), name='consulta_informe'),
    # path('load_sint_csv/', views.load_sint_csv, name='load_sint_csv'), #! Descomentar para realizar la carga de la BBDD
    # path('load_pat_csv/', views.load_pat_csv, name='load_pat_csv'), #! Descomentar para realizar la carga de la BBDD
    path('datos_paciente/', login_required(views.datos_paciente), name='datos_paciente'),
    path('patologias/', login_required(views.patologias_form), name='patologias'),
    path('sintomas/', login_required(views.sintomas_form), name='sintomas'),
    path('', views.Login.as_view(), name='login'),
    path('logout/', login_required(views.logout_usuario), name='logout'),
    path('index/', login_required(views.index), name='index'),
    path('info_list/', login_required(views.info_list), name='info_list'),
    path('info_details/', login_required(views.info_details), name='info_details'),
    path('info_delete/<int:id>', login_required(views.delete_informe), name='info_delete'),
    path('user_list/', login_required(views.user_list), name='user_list'),
    path('user_details/', login_required(views.user_details), name='user_details'),
    path('user_delete/<int:id>', login_required(views.user_delete), name='user_delete'),
]