
from ..utilidades import  updateEstado, updateH
from django.shortcuts import render, redirect
from ..models import Das, Importacion,Mercancia,Factura_proveedor,Proveedor
import numpy as np 
from django.contrib import messages 

def startFactProve(request,id):
    if request.method=='POST':
        idf=Factura_proveedor.objects.filter(importacion=id)
        #fc=Importacion.objects.get(id = 365)
        num_proveedor= request.POST.get('num_proveedor')
        prove= request.POST.getlist('proveedor')
        if len(prove)!=1:
            result=np.unique(prove) 
            if len(result)< int(num_proveedor):
                messages.error(request, "El proveedor debe ser distinto")
                fp=Factura_proveedor.objects.filter(importacion=id)
                proveedores=Proveedor.objects.select_related().all()
                cant=""
                for i in range(len(fp)):
                    cant=cant+str(fp[i].id)+";"
                datos={"id":id,
                        "proveedores":proveedores,
                        "facturaProveedor":fp,
                        "cant1":len(fp),
                        "cant":cant}
                return render(request,'core/proveedor.html',datos)
        print("valor de proveedor",prove)
        ncajas=request.POST.getlist('ncajas')
        v_envio=request.POST.getlist('v_envio')
        v_factura=request.POST.getlist('v_factura')
        comis_envio=request.POST.getlist('comis_envio')
        comis_tarjeta=request.POST.getlist('comis_tarjeta')
        isd=request.POST.getlist('isd')
        t_pago=request.POST.getlist('t_pago')
        extra=request.POST.getlist('extra')
        idfp=[]
        for i in range(len(idf)):            
            idfp.append(idf[i].id)
        respuesta=saveFacuturaProveedor(idfp,prove,id,ncajas,v_envio,v_factura,comis_envio,comis_tarjeta,isd,t_pago,extra)
        updateEstado(id,1)
        updateH(id,0,0,1)
        da=Das.objects.filter(importacion=id).first()
        if da!=None:
            idas=da.id
            return redirect ('datosdas',id,idas)
        else:
            return redirect ('startdas',id)               
    else:
        fp=Factura_proveedor.objects.filter(importacion=id)
        proveedores=Proveedor.objects.select_related().all()
        cant=""
        for i in range(len(fp)):
            print("el tamaño de ñ cantidad es ",fp[i].id)
            cant=cant+str(fp[i].id)+";"

        datos={"id":id,
                "proveedores":proveedores,
                "facturaProveedor":fp,
                "cant1":len(fp),
                "cant":cant}
    return render(request,'core/proveedor.html',datos)

def saveFacuturaProveedor(idfp,prove,id,ncajas,v_envio,v_factura,comis_envio,comis_tarjeta,isd,t_pago,extra):
    for j in range (len(prove)):
        fp = Factura_proveedor()
        fp.id=idfp[j]
        fp.proveedor=Proveedor.objects.get(id = prove[j])
        fp.importacion=Importacion.objects.get(id=id)
        fp.num_cajas=ncajas[j]
        fp.valor_factura=v_factura[j]
        fp.valor_envio=v_envio[j]
        fp.comision_envio=comis_envio[j]
        fp.comision_tarjeta=comis_tarjeta[j]
        fp.isd=isd[j]
        fp.total_pago=t_pago[j]
        fp.extra=extra[j]
        
        fp.save() 
    return {'error':False}

