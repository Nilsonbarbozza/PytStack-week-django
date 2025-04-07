from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from mentorados.models import Mentorados

class DisponibilidadeHorarios(models.Model):
    data_inicial = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    agendado = models.BooleanField(default=False)

    @property
    def data_final(self):
        return self.data_inicial + timedelta(minutes=50)
    
class Reuniao(models.Model):
    tag_choices = (
        ('G', 'Gestão'),
        ('M', 'Marketing'),
        ('RH', 'Gestão de pessoas'),
        ('I', 'Impostos')
    )

    data = models.ForeignKey(DisponibilidadeHorarios, on_delete=models.CASCADE)
    mentorado = models.ForeignKey(Mentorados, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=tag_choices)
    descricao = models.TextField()
