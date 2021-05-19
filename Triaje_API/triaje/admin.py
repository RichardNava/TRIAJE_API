from django.contrib import admin

from .models import Paciente, Sintoma, Patologia, DetalleInforme, Informe

admin.site.register(Paciente)
admin.site.register(Sintoma)
admin.site.register(Patologia)
admin.site.register(Informe)
admin.site.register(DetalleInforme)

