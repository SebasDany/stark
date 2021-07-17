from ..controlador import saveAfianzado, saveDetalleAfianzado
from django.shortcuts import render, redirect
from ..models import Factura_afianzado

def datosAfianzado(request):
    
    afianzado=request.POST.get('afianzado')
    importacion=request.POST.get('idfechaImport')
    fecha=request.POST.get('fecha')
    numero=request.POST.get('numero')
    subtotal=request.POST.get('subtotal')
    respuesta=saveAfianzado(afianzado,importacion,fecha,numero,subtotal)
    
    return render(request,'core/detalle_afianzado.html',respuesta)

def detalleAfianzado(request):
    af=request.POST.getlist('id_afianzado')
    print("················ ", af)
    desc=request.POST.getlist('descripcion')
    ape=request.POST.getlist('alpeso')
    apr=request.POST.getlist('alprecio')
    iv=request.POST.getlist('iva')
    t=request.POST.getlist('total')
    respuesta=saveDetalleAfianzado(af,desc,ape,apr,iv,t)
      
       
        
    return render(request,'core/detalle_importacion.html',respuesta)