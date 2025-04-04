from django.shortcuts import render
from django.http import HttpResponse

def mentorados(request):
    if request.method == 'GET':
        return render(request, 'teste.html')
