from django.contrib import admin
from .models import DisponibilidadeHorarios, Reuniao, Tarefa, Upload

admin.site.register(DisponibilidadeHorarios)
admin.site.register(Reuniao)
admin.site.register(Tarefa)
admin.site.register(Upload)

