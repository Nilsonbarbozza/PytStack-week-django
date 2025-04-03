from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth

def cadastro(request):
   if request.method == 'GET':
      return render(request, 'cadastro.html')
   else:
      # Valores pegos do meu forms
      username = request.POST.get('username')
      senha = request.POST.get('senha')
      confirmar_senha = request.POST.get('confirmar_senha')
      
      if not senha == confirmar_senha:
         messages.add_message(request, constants.ERROR, 'Senha e confirmar senha devem ser iguais.')
         return redirect('cadastro')

      if len(senha) < 6:
         messages.add_message(request, constants.ERROR, 'Senha deve conter mais de 6 caracteres.')
         return redirect('cadastro')
   
      users = User.objects.filter(username=username)
      if users.exists():
         messages.add_message(request, constants.ERROR, 'Esse usuario já existe!')
         return redirect('cadastro')

      User.objects.create_user(
      username=username,
      password=senha
      )
   messages.add_message(request, constants.SUCCESS, 'CADASTRO REALIZADO COM SUCESSO!')
   return redirect('login')

def login(request):
   if request.method == 'GET':
      return render(request, 'login.html')
   else:
      username = request.POST.get('username')
      senha = request.POST.get('senha')
      
      user = authenticate(request, username=username, password=senha)
   
   if user:
      auth.login(request, user)
      return redirect('/mentorados/')

   messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
   return redirect('login')