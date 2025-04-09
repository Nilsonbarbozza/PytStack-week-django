from django.db import models
from django.contrib.auth.models import User
import secrets

class Navigators(models.Model):
    nome = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome
    
class Mentorados(models.Model):
    estagio_choices = (
        ('E1', '10-100k'),
        ('E2', '100-1KK')
    )

    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    estagio = models.CharField(max_length=2, choices=estagio_choices)
    navigator = models.ForeignKey(Navigators, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=16, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token: 
            self.token = self.gerar_token_unico()
        super().save(*args, **kwargs)

    def gerar_token_unico(self):
        while True:
            token = secrets.token_urlsafe(8)  
            if not Mentorados.objects.filter(token=token).exists():
                return token
    
    def __str__(self):
        return self.nome

