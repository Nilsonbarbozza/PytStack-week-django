from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import DisponibilidadeHorarios, Reuniao, Tarefa, Upload
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, Http404
from mentorados.models import Mentorados
from .auth import valida_token
from babel.dates import format_date
import locale
from django.views.decorators.csrf import csrf_exempt


locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def reunioes(request):
    if request.method == 'GET':
        reunioes = Reuniao.objects.filter(
            data__mentor=request.user
        )
        return render(request, 'reunioes.html', {'reunioes':reunioes})
    else:
        data = request.POST.get('data')

        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')

        disponibilidades = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=(data - timedelta(minutes=50)),
            data_inicial__lte=(data + timedelta(minutes=50))
        )

        if disponibilidades.exists():
            messages.add_message(request, constants.ERROR, 'Você já possui uma reunião em aberto.')
            return redirect('reunioes')
        

        disponibilidade = DisponibilidadeHorarios(
            data_inicial=data,
            mentor=request.user

        )

        disponibilidade.save()
        

        messages.add_message(request, constants.SUCCESS, 'Horário disponibilizado com sucesso.')
        return redirect('reunioes')

def auth(request):
    if request.method == 'GET':
        return render(request, 'auth_mentorado.html')
    else:
        token = request.POST.get('token')

        if not Mentorados.objects.filter(token=token).exists():
            messages.add_message(request, constants.ERROR, 'Token inválido')
            return redirect('auth_mentorado')
        
        response = redirect('escolher_dia')
        response.set_cookie('auth_token', token, max_age=3600)
        return response
    

def escolher_dia(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    if request.method == 'GET':
        mentorado = valida_token(request.COOKIES.get('auth_token'))
        disponibilidades = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=datetime.now(),
            agendado=False,
            mentor=mentorado.user
        ).values_list('data_inicial', flat=True)

        datas = []
        datas_vistas = set()

        for data in disponibilidades:
            data_formatada = data.date()
            data_str = data_formatada.strftime('%d-%m-%Y')

            if data_str not in datas_vistas:
                datas_vistas.add(data_str)
                datas.append({
                    'data_completa': data_str,
                    'dia_semana': format_date(data_formatada, 'EEEE', locale='pt_BR'),
                    'mes': format_date(data_formatada, 'MMMM', locale='pt_BR').capitalize()
                })

        return render(request, 'escolher_dia.html', {'horarios': datas})

    
def agendar_reuniao(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    
    if request.method == 'GET':
        data = request.GET.get("data")
        data = datetime.strptime(data, '%d-%m-%Y')
        mentorado = valida_token(request.COOKIES.get('auth_token'))
        horarios = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=data,
            data_inicial__lt=data + timedelta(days=1),
            agendado=False,
            mentor=mentorado.user
        )
  
        return render(request, 'agendar_reuniao.html', {'horarios': horarios, 'tags': Reuniao.tag_choices})
    else:
        horario_id = request.POST.get('horario')
        tag = request.POST.get('tag')
        descricao = request.POST.get("descricao")

        #TODO: Realizar validações

        reuniao = Reuniao(
            data_id=horario_id,
            mentorado=valida_token(request.COOKIES.get('auth_token')),
            tag=tag,
            descricao=descricao
        )
        reuniao.save()

        horario = DisponibilidadeHorarios.objects.get(id=horario_id)
        horario.agendado = True
        horario.save()

        messages.add_message(request, constants.SUCCESS, 'Reunião agendada com sucesso.')
        return redirect('escolher_dia')

def tarefa(request, id):
    mentorado = Mentorados.objects.get(id=id)
    if mentorado.user != request.user:
        raise Http404()
    
    if request.method == 'GET':
        tarefas = Tarefa.objects.filter(mentorado=mentorado)
        
        return render(request, 'tarefa.html', {'mentorado': mentorado, 'tarefas': tarefas})    
    
    else:
        tarefa = request.POST.get('tarefa')

        t = Tarefa(
        mentorado=mentorado,
        tarefa=tarefa,
        )
        t.save()

        return redirect(f'/reunioes/tarefa/{mentorado.id}')

def upload(request, id):
    mentorado = Mentorados.objects.get(id=id)
    
    
    if mentorado.user != request.user:
        raise Http404()
    
    
    
    video = request.FILES.get('video')
    upload = Upload(
        mentorado=mentorado,
        video=video
    )
    
    upload.save()
    return redirect(f'/reunioes/tarefa/{mentorado.id}')

def tarefa_mentorado(request):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')
    
    if request.method == 'GET':
        videos = Upload.objects.filter(mentorado=mentorado)
        tarefas = Tarefa.objects.filter(mentorado=mentorado)
    
    return render(request, 'tarefa_mentorado.html', {'mentorado': mentorado, 'videos': videos, 'tarefas': tarefas})


@csrf_exempt
def tarefa_alterar(request, id):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')

    tarefa = Tarefa.objects.get(id=id)
    if mentorado != tarefa.mentorado:
        raise Http404()
    tarefa.realizada = not tarefa.realizada
    tarefa.save()

    return HttpResponse('teste')    