from core.view.gestorImportacion import importacion
from ..controlador import saveAfianzado, saveDetalleAfianzado
from django.shortcuts import render, redirect
from ..models import Detalle_afianzado, Factura_afianzado,Importacion,Afianzado
import datetime

def startAfianzado(request,id,idas):
    fecha=str(datetime.datetime.today()).split()[0]
    imprt=Importacion.objects.get(id=id)
    fa=Factura_afianzado(importacion=imprt,fecha=fecha,numero=0,subtotal=0)
    fa.save()
    
    as_af=Factura_afianzado.objects.last()
    idfa=as_af.id
    
    return redirect('datosafianzado',id,idas,idfa)

    
    #fianzado=Afianzado.objects.all()
    #return render(request,'core/factura_afianzado.html',{'afianzado':afianzado})

def datosAfianzado(request,id,idas,idfa):
    
    print("estoy dentro del datos afianzado")

    if request.method=='POST':
    
        afianzado=request.POST.get('afianzado')
        importacion=request.POST.get('idfechaImport')
        fecha=request.POST.get('fecha')
        numero=request.POST.get('numero')
        subtotal=request.POST.get('subtotal')
        saveAfianzado(idfa,afianzado,id,fecha,numero,subtotal)
        
        return redirect('creardetalleafianzado',id,idas,idfa)
    afianzado=Afianzado.objects.all()
    faf=Factura_afianzado.objects.get(importacion=id)

    
    datos={"id":id,
            
            "faf":faf,
            "afianzado":afianzado,"id":id,
        "idfa":idfa,
        "idas":idas

    }
    
    return render(request,'core/factura_afianzado.html',datos)
    #return render(request,'core/detalle_afianzado.html',respuesta)

def crearDetalleAfianzado(request,id,idas,idfa):
    dA=Detalle_afianzado.objects.filter(factura_afianzado=idfa).first()
    if dA == None:
        f_afianzado=Factura_afianzado.objects.get(id=idfa)
        for i in range(4):
        
            dta=Detalle_afianzado(factura_afianzado=f_afianzado,descripcion="____",al_peso=0,al_precio=0,iva=0,total=0)
            dta.save()

    return redirect('detalleafianzado',id,idas,idfa) 

def detalleAfianzado(request,id,idas,idfa):
    if request.method=='POST':
        idd=Detalle_afianzado.objects.filter(factura_afianzado=idfa)#obtiene los datos de la importacion actual
        
        desc=request.POST.getlist('descripcion')
        ape=request.POST.getlist('alpeso')
        apr=request.POST.getlist('alprecio')
        iv=request.POST.getlist('iva')
        t=request.POST.getlist('total')
        idda=[]
        for i in range(len(idd)):
            
            idda.append(idd[i].id)
        saveDetalleAfianzado(id,idda,desc,ape,apr,iv,t)
        return redirect('detalleimportacion',id,idas,idfa)
        #return render(request,'core/detalle_importacion.html')
        

    else:

        dat_d=Detalle_afianzado.objects.filter(factura_afianzado=idfa)
        afz=Factura_afianzado.objects.get(importacion=id)
        print("si encontre datoe ne el factura afianzado",afz)

        factAf=Detalle_afianzado.objects.filter(factura_afianzado=idfa)
        
        cant=""
        for i in range(len(factAf)):
            print("el tamaño de ñ cantidad es ",factAf[i].id)
            cant=cant+str(factAf[i].id)+";"
        
        dato={ "dat_d":dat_d,
            "afz":afz,
            "id":id,
            "idfa":idfa,
            "idas":idas,
            "cant":cant


        }
        
    return render(request,'core/detalle_afianzado.html',dato)  
    #return render(request,'core/detalle_importacion.html')