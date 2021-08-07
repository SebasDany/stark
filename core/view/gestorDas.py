
from ..controlador import  subtotal1, updateEstado, updateH
from django.shortcuts import render, redirect
from ..models import Detalle_das, Factura_afianzado, Importacion,Mercancia,Afianzado,Das, Producto,Proveedor_producto
import datetime

def startDas(request,id):
    d2=Das.objects.all()
    fecha=str(datetime.datetime.today()).split()[0]
    importacion=Importacion.objects.get(id=id)
    das=Das(importacion= importacion,numero_atribuido=0,numero_entrega=0,fecha_embarque=fecha,
    fecha_llegada=fecha,documento_transporte="--",tipo_carga="--",pais_procedncia="--",
    via_transporte="--",puerto_enbarque="--",ciudad_importador="--",empresa_tranporte="--",
    identificacion_carga="--")
    das.save()
    d=Das.objects.last()     
    return redirect('datosdas',id,d.id)

def datosDas(request,id,idas):
    if request.method=='POST':
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
        updateEstado(id,2)
        updateH(id,idas,0,2)
        objDas=Das.objects.last()
        m=Mercancia.objects.last()
        dd=Detalle_das.objects.filter(das=idas)
        print("cantidad",cantidad)
        if(len(dd) < int(cantidad)):
                for k in  range(int(cantidad)-len(dd)):
                    dt=Detalle_das(mercancia=m,das=objDas,advalorem1=0,fodinfa1=0,iva1=0)
                    dt.save()
        return redirect('detalledas',id,idas)
    else:
        das=Das.objects.get(id=idas)
        datos={"id":id,
                "das":das
                }
    return render(request,'core/das.html',datos)

def detalleDas(request,id,idas):
    if request.method=='POST':
        id_d=Detalle_das.objects.filter(das=idas)
        mercancia=request.POST.getlist('mercancia')
        advalorem=request.POST.getlist('advalorem')
        fodinfa=request.POST.getlist('fodinfa')
        iva=request.POST.getlist('iva')
        sub_total=request.POST.getlist('sub_total')
        id_dd=[]
        for i in range(len(id_d)):    
            id_dd.append(id_d[i].id)
        saveDetalleDas(id_dd,idas,mercancia,advalorem,fodinfa,iva,sub_total)
        updateEstado(id,3)
        updateH(id,idas,0,3)
        fa=Factura_afianzado.objects.filter(importacion=id).first()
        if(fa!=None):
            idfa=fa.id
            return redirect('datosafianzado',id,idas,idfa)
        else:
            return redirect('startafianzado',id,idas)
    else: 
        dd=Detalle_das.objects.filter(das=idas)
        mercancias=Mercancia.objects.select_related().all()
        dtd=Detalle_das.objects.filter(das=idas)
        cant=""
        for i in range(len(dtd)):
            print("el tamaño de ñ cantidad es ",dtd[i].id)
            cant=cant+str(dtd[i].id)+";"
        datos={"id":id,"idas":idas,
                "ddas":dd,'mercancia':mercancias,
                "cant":cant
        }
    return render (request, 'core/detalle_das.html',datos)

def saveDas(idas,idfechaImport,numero_atribuido,numero_entrega,
fecha_embarque,fecha_llegada,documento_transporte,
tipo_carga,pais_procedncia,via_transporte,puerto_enbarque,
ciudad_importador,empresa_tranporte,identificacion_carga,
monto_flete,total_items,peso_neto,total_bultos,unidades_comerciales,
total_tributos,valor_seguros,cif,peso_bruto,unidades_fisicas,valor_fob):
    das = Das()
    das.importacion=Importacion.objects.get(id=idfechaImport)
    das.numero_atribuido=numero_atribuido
    das.numero_entrega=numero_entrega
    das.fecha_embarque=fecha_embarque
    das.fecha_llegada=fecha_llegada
    das.documento_transporte=documento_transporte
    das.tipo_carga=tipo_carga
    das.pais_procedncia=pais_procedncia
    das.via_transporte=via_transporte
    das.puerto_enbarque=puerto_enbarque
    das.ciudad_importador=ciudad_importador  
    das.empresa_tranporte=empresa_tranporte
    das.identificacion_carga=identificacion_carga
    das.monto_flete=monto_flete
    das.total_items=total_items
    das.peso_neto=peso_neto
    das.total_bultos=total_bultos
    das.unidades_comerciales=unidades_comerciales
    das.total_tributos=total_tributos 
    das.valor_seguros=valor_seguros
    das.cif=cif
    das.peso_bruto=peso_bruto
    das.unidades_fisicas=unidades_fisicas
    das.valor_fob=valor_fob
    das.id=idas
    das.save() #Contiene una realcion de uno auno
    return {'error':False}

def saveDetalleDas(id_dd,idas,mercancia=[],advalorem=[],fodinfa=[],iva=[],sub_total=[]):
    das=Das.objects.get(id=idas)# obtiene el utlimo dato del la consulta
    for i in  range(len(mercancia)):
        dD=Detalle_das()
        dD.mercancia=Mercancia.objects.get(id = mercancia[i])
        dD.das=das
        dD.advalorem1=advalorem[i]
        dD.fodinfa1=fodinfa[i]
        dD.iva1=iva[i]
        dD.subtotal1=sub_total[i]
        dD.id=id_dd[i]
        dD.save()
 
    return {'error':False}

def updateSubtotal1(id_dd,sub1):
    for i in range(len(id_dd)):
        Detalle_das.objects.filter(id=id_dd[i]).update(subtotal1=sub1[i])

    return 1

