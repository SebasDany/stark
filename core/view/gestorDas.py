from ..controlador import saveFacuturaProveedor, saveDas,saveDetalleDas
from django.shortcuts import render, redirect
from ..models import Importacion,Mercancia,Afianzado





def datosDas(request):
    importacion=request.POST.get('idfechaImport')
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
    saveDas(importacion,numero_atribuido,numero_entrega,fecha_embarque,
    fecha_llegada,documento_transporte,tipo_carga,pais_procedncia,
    via_transporte,puerto_enbarque,ciudad_importador,empresa_tranporte,
    identificacion_carga,monto_flete,total_items,peso_neto,total_bultos,
    unidades_comerciales,total_tributos,valor_seguros,cif,peso_bruto,
    unidades_fisicas,valor_fob)

    cantidad=request.POST.get('cantidad')
    cant=[]
    for k in  range(int(cantidad)):
        cant.append(k)
    print(cantidad)
    mercancias=Mercancia.objects.select_related().all()
    return render (request, 'core/detalle_das.html',{'cantidad':cant,'mercancia':mercancias})

def detalleDas(request):
    mercancia=request.POST.getlist('mercancia')
    advalorem=request.POST.getlist('advalorem')
    fodinfa=request.POST.getlist('fodinfa')
    iva=request.POST.getlist('iva')

    saveDetalleDas(mercancia,advalorem,fodinfa,iva)
    fecha=Importacion.objects.last()
    afianzado=Afianzado.objects.all()
        

    return render(request,'core/factura_afianzado.html',{'fecha':fecha,'afianzado':afianzado})