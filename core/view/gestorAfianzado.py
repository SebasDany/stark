
from ..controlador import  updateEstado, updateH
from django.shortcuts import render, redirect
from ..models import Detalle_afianzado, Factura_afianzado,Importacion,Afianzado, Mercancia, Producto, Proveedor
import datetime

def startAfianzado(request,id,idas):
    fecha=str(datetime.datetime.today()).split()[0]
    imprt=Importacion.objects.get(id=id)
    fa=Factura_afianzado(importacion=imprt,fecha=fecha,numero=0,subtotal=0)
    fa.save()
    as_af=Factura_afianzado.objects.last()
    idfa=as_af.id
    return redirect('datosafianzado',id,idas,idfa)

def datosAfianzado(request,id,idas,idfa):
    if request.method=='POST':
        afianzado=request.POST.get('afianzado')
        importacion=request.POST.get('idfechaImport')
        fecha=request.POST.get('fecha')
        numero=request.POST.get('numero')
        subtotal=request.POST.get('subtotal')
        saveAfianzado(idfa,afianzado,id,fecha,numero,subtotal)
        updateEstado(id,4)
        updateH(id,idas,idfa,4)
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
        updateEstado(id,5)
        updateH(id,idas,idfa,5)
        return redirect('detalleimportacion',id,idas,idfa)
    else:
        dat_d=Detalle_afianzado.objects.filter(factura_afianzado=idfa)
        afz=Factura_afianzado.objects.get(importacion=id)
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

def saveAfianzado(idaf,afianzado,idfechaImport,fecha,numero,subtotal):
    af=Factura_afianzado()
    af.afianzado=Afianzado.objects.get(id=afianzado)
    af.importacion=Importacion.objects.get(id=idfechaImport)
    af.fecha=fecha
    af.numero=numero
    af.subtotal=subtotal
    af.id=idaf
    af.save() #Descomentar relacion de uno a uno entre eimprotaacion y factua afianzado
    afz=Factura_afianzado.objects.last()
    cant=[]
    for k in  range(4):
        cant.append(k)
    return {'error':False,
            'cantidad':cant, 
            'afz':afz
            }
def saveDetalleAfianzado(id,idda,desc=[],ape=[],apr=[],iv=[], t=[]):
    faf=Factura_afianzado.objects.get(importacion=id)
    for i in  range(len(ape)):
        dA=Detalle_afianzado()
        dA.factura_afianzado=faf
        dA.descripcion=desc[i]
        dA.al_peso=ape[i]
        dA.al_precio=apr[i]
        dA.iva=iv[i]
        dA.total=t[i]
        dA.id=idda[i]
        dA.save()
        productos=Producto.objects.select_related().all()
        proveedores=Proveedor.objects.select_related().all()
        mercancias=Mercancia.objects.select_related().all()
    return {'error':False,
            "productos":productos,
            "proveedores":proveedores,
            "mercancias":mercancias
            }