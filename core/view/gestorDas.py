from core.view.gestorImportacion import importacion
from ..controlador import saveFacuturaProveedor, saveDas,saveDetalleDas
from django.shortcuts import render, redirect
from ..models import Detalle_das, Factura_afianzado, Importacion,Mercancia,Afianzado,Das, Producto,Proveedor_producto
import datetime

def startDas(request,id):
    d2=Das.objects.all()
    
    fecha=str(datetime.datetime.today()).split()[0]
    print("verificando si existe datos das ")
    
    print("verificando si existe datos das ", )
    

    importacion=Importacion.objects.get(id=id)
    das=Das(importacion= importacion,numero_atribuido=0,numero_entrega=0,fecha_embarque=fecha,
    fecha_llegada=fecha,documento_transporte="--",tipo_carga="--",pais_procedncia="--",
    via_transporte="--",puerto_enbarque="--",ciudad_importador="--",empresa_tranporte="--",
    identificacion_carga="--")
    das.save()
    d=Das.objects.last()
    verifi=Das.objects.get(importacion=id)
    
    
    datos={"idas":verifi.id,'fecha':fecha,"id":id
    }
    return redirect('datosdas',id,d.id)

def datosDas(request,id,idas):
    if request.method=='POST':

        print("estoy dentro del post del das ####")
        
        numero_atribuido=request.POST.get('numero_atribuido')
        numero_entrega=request.POST.get('numero_entrega')
        fecha_embarque=request.POST.get('fecha_embarque')
        fecha_llegada=request.POST.get('fecha_llegada')
        documento_transporte=request.POST.get('documento_transporte')
        tipo_carga=request.POST.get('tipo_carga')
        pais_procedncia=request.POST.get('pais_procedncia')
        via_transporte=request.POST.get('via_transporte')
        puerto_enbarque=request.POST.get('puerto_enbarque')
        ciudad_importador=request.POST.get('ciudad_importador')
        empresa_tranporte=request.POST.get('empresa_tranporte')
        identificacion_carga=request.POST.get('identificacion_carga')
        monto_flete=request.POST.get('monto_flete')
        total_items=request.POST.get('total_items')
        peso_neto=request.POST.get('peso_neto')
        total_bultos=request.POST.get('total_bultos')
        unidades_comerciales=request.POST.get('unidades_comerciales')
        total_tributos=request.POST.get('total_tributos')
        valor_seguros=request.POST.get('valor_seguros')
        cif=request.POST.get('cif')
        peso_bruto=request.POST.get('peso_bruto')
        unidades_fisicas=request.POST.get('unidades_fisicas')
        valor_fob=request.POST.get('valor_fob')
        cantidad=request.POST.get('cantidad')
        saveDas(idas,id,numero_atribuido,numero_entrega,fecha_embarque,
        fecha_llegada,documento_transporte,tipo_carga,pais_procedncia,
        via_transporte,puerto_enbarque,ciudad_importador,empresa_tranporte,
        identificacion_carga,monto_flete,total_items,peso_neto,total_bultos,
        unidades_comerciales,total_tributos,valor_seguros,cif,peso_bruto,
        unidades_fisicas,valor_fob)
        objDas=Das.objects.last()
        m=Mercancia.objects.last()
        dd=Detalle_das.objects.filter(das=idas)
        if(len(dd) < int(cantidad)):
                print(len(dd),int(cantidad))
                print(len(dd)-int(cantidad))
            
                for k in  range(int(cantidad)-len(dd)):
                    dt=Detalle_das(mercancia=m,das=objDas,advalorem1=0,fodinfa1=0,iva1=0)
                    dt.save()
        
        

        return redirect('detalledas',id,idas)
    else:
        
    
        #print(context)
        das=Das.objects.get(id=idas)
        datos={"id":id,
            "das":das
    }

    return render(request,'core/das.html',datos)
def datosDas1(request):
    # importacion=request.POST.get('idfechaImport')
    # numero_atribuido=request.POST.get('numero_atribuido')
    # numero_entrega=request.POST.get('numero_entrega')
    # fecha_embarque=request.POST.get('fecha_embarque')
    # fecha_llegada=request.POST.get('fecha_llegada')
    # documento_transporte=request.POST.get('documento_transporte')
    # tipo_carga=request.POST.get('tipo_carga')
    # pais_procedncia=request.POST.get('pais_procedncia')
    # via_transporte=request.POST.get('via_transporte')
    # puerto_enbarque=request.POST.get('puerto_enbarque')
    # ciudad_importador=request.POST.get('ciudad_importador')
    # empresa_tranporte=request.POST.get('empresa_tranporte')
    # identificacion_carga=request.POST.get('identificacion_carga')
    # monto_flete=request.POST.get('monto_flete')
    # total_items=request.POST.get('total_items')
    # peso_neto=request.POST.get('peso_neto')
    # total_bultos=request.POST.get('total_bultos')
    # unidades_comerciales=request.POST.get('unidades_comerciales')
    # total_tributos=request.POST.get('total_tributos')
    # valor_seguros=request.POST.get('valor_seguros')
    # cif=request.POST.get('cif')
    # peso_bruto=request.POST.get('peso_bruto')
    # unidades_fisicas=request.POST.get('unidades_fisicas')
    # valor_fob=request.POST.get('valor_fob')
    # saveDas(importacion,numero_atribuido,numero_entrega,fecha_embarque,
    # fecha_llegada,documento_transporte,tipo_carga,pais_procedncia,
    # via_transporte,puerto_enbarque,ciudad_importador,empresa_tranporte,
    # identificacion_carga,monto_flete,total_items,peso_neto,total_bultos,
    # unidades_comerciales,total_tributos,valor_seguros,cif,peso_bruto,
    # unidades_fisicas,valor_fob)

    cantidad=4
    cant=[]
    for k in  range(int(cantidad)):
        cant.append(k)
    print(cantidad)
    mercancias=Mercancia.objects.select_related().all()
    return render (request, 'core/detalle_das.html',{'cantidad':cant,'mercancia':mercancias})



def detalleDas(request,id,idas):
    if request.method=='POST':
        
        id_d=Detalle_das.objects.filter(das=idas)
        print("ESTOY DNTRO DEL PSOT DEL DEATLLE DAS")

        mercancia=request.POST.getlist('mercancia')
        advalorem=request.POST.getlist('advalorem')
        fodinfa=request.POST.getlist('fodinfa')
        iva=request.POST.getlist('iva')
        id_dd=[]
        for i in range(len(id_d)):
            
            id_dd.append(id_d[i].id)

        saveDetalleDas(id_dd,idas,mercancia,advalorem,fodinfa,iva)

        fa=Factura_afianzado.objects.filter(importacion=id).first()
        if(fa!=None):
            idfa=fa.id
            return redirect('datosafianzado',id,idas,idfa)
        else:
            return redirect('startafianzado',id,idas)

    else:
        
        print("estoy dentro del detallae das")

        

        
        dd=Detalle_das.objects.filter(das=idas)
        mercancias=Mercancia.objects.select_related().all()

        
        datos={"id":id,"idas":idas,
                "ddas":dd,'mercancia':mercancias,
        }

    
    
    
    return render (request, 'core/detalle_das.html',datos)