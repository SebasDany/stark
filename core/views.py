from django.shortcuts import render, redirect

from .models import Historial
from django.contrib import messages


# Create your views here.

def inicio(request):
    return render(request,'core/inicio.html')
def home(request):
    #i=Importacion.objects.all()
    historial=Historial.objects.order_by('-id')[:4]
    allimport=Historial.objects.all() 
    ultimo=Historial.objects.last()

    datos={
        "importaciones":historial,
        "allimport":allimport,
        "ultimo":ultimo
         }
    if(historial==None):
        datos={
        "importaciones":0 }
        datos.update(datos) 

    return render(request,'core/home.html',datos)

def login(request):
    return render(request,'core/login.html')
