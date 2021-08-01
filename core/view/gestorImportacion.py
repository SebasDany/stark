


from core.view.gestorDas import updateSubtotal1
from core.sincronizacion import Productos2Woocommerce
from core.models import Das, Detalle_das, Detalle_importacion, Factura_proveedor, Importacion, Mercancia, Producto, Proveedor
from ..controlador import  aranceles, costo_unitario, costos, incrementos, porcentuales, subtotal1, subtotal2, updateEstado, updateH
from django.shortcuts import render, redirect
from django.http import HttpResponse
import numpy as np 
from django.contrib import messages 

def iniciarProduct(request):
    dtp=Detalle_importacion()
    dtp.save()
    return redirect('productosimportados')

def detalleImportacion(request,id,idas,idfa):
    datos={ "id":id,
            "idfa":idfa,
            "idas":idas }
    return render(request,'core/detalle_importacion.html',datos)
 
def addProductImport(request,id,idas,idfa):#guarda los productos importados en la base
    if request.method=='POST':
        if "id_producto" in request.POST:
            sku=request.POST.getlist('id_producto')
            print(sku)
            guardarProductoImport(sku,id)
            updateEstado(id,6)
            updateH(id,idas,idfa,6)
    return redirect('viewproduct',id,idas,idfa)

def viewProduct(request,id,idas,idfa):#vista de los producto importadosde de la base
    pr=Detalle_importacion.objects.filter(importacion=id)
 
    proveedores=Factura_proveedor.objects.filter(importacion=id).distinct()
    print (proveedores)
    mercancias=Detalle_das.objects.filter(das=idas)
    datos={
                "id":id,
                "idas":idas,
                "idfa":idfa,
                'error':False,
                "productos":pr,
                "proveedores":proveedores,
                "mercancias":mercancias
            }
    return render(request, 'core/crear_importacion.html', datos ) 

def productosImportados(request,id,idas,idfa):
    if request.method=='POST':
        
        product_id=request.POST.getlist('id_producto')  
        id_df=request.POST.getlist('id_df') 
        print(product_id)
        print(id_df)
        precio=request.POST.getlist('precio')
        proveedor=request.POST.getlist('proveedor')
        cantidad=request.POST.getlist('cantidad')
        
        mercancia=request.POST.getlist('mercancia')
        peso=request.POST.getlist('peso')
        vector=np.zeros(len(product_id))
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector)
        subtotal=subtotal2(id)
        print("id_df id",id_df)
        
        saveDetalleImportacion(id,subtotal["producto_id"],peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"],vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector)
        print("subtotal id",subtotal["producto_id"])
        subt1=subtotal1(id)
        updateSubtotal1(subt1["id_dd"],subt1["sub1_merc_t"])
        arancel=aranceles(id)
        saveDetalleImportacion(id,arancel["producto_id"],peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],vector,vector,vector,vector,vector,vector,vector,vector,vector)
        print("arancel id",arancel["producto_id"])
        porcent=porcentuales(id)
        saveDetalleImportacion(id,porcent["producto_id"],peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], vector,vector,vector,vector, vector,vector)
        print("porcent total id",porcent["producto_id"])
        costo=costos(id)
        saveDetalleImportacion(id,costo["producto_id"],peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], costo["costo1"],costo["costo2"],costo["costo3"],vector,vector,vector)
        print("costo id",costo["producto_id"])
        costo_unit=costo_unitario(id)
        saveDetalleImportacion(id,costo_unit["producto_id"],peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], costo["costo1"],costo["costo2"],costo["costo3"],costo_unit["costo1_unitario"],vector,vector)
        print("costo_unit id",costo_unit["producto_id"])
        incremento=incrementos(id)
        saveDetalleImportacion(id,incremento["producto_id"],peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], costo["costo1"],costo["costo2"],costo["costo3"],costo_unit["costo1_unitario"], incremento["inc_porcentual"],incremento["inc_dolares"] )
        print("incremento id",incremento["producto_id"])
        print("Subtotal",subtotal["SumaSub2"], subt1["suma_sub1"])
        print("Subtotal",subtotal["SumaSub2"], subt1["suma_sub1"])
        print("Subtotal",subtotal["SumaSub2"], subt1["suma_sub1"])
        
        if(subtotal["SumaSub2"]!=subt1["suma_sub1"]):
            messages.error(request, "Validación INCORRECTA de suma de subtotales. Revisar los datos")
            return redirect('viewproduct',id,idas,idfa)
        elif(arancel["suma_ad"]!=subt1["ad_das"]):
                messages.error(request, "Validación INCORRECTA de suma de Advalorem. Revisar los datos")
                return redirect('viewproduct',id,idas,idfa)
                
        elif(arancel["suma_fod"]!=subt1["fod_das"]):
                messages.error(request, "Validación INCORRECTA de suma de Fodinfa. Revisar los datos")
                return redirect('viewproduct',id,idas,idfa)
        elif(arancel["suma_iva"]!=subt1["iva_das"]):
                messages.error(request, "Validación INCORRECTA de suma de Iva. Revisar los datos")
                return redirect('viewproduct',id,idas,idfa)
        else:
            messages.success(request, "Validación correcta ")
            updateEstado(id,7)
            updateH(id,idas,idfa,7)
            return redirect( 'viewresults',id,idas,idfa )
       
       

    return 1

def viewResults(request,id,idas,idfa):
    if request.method=='POST':
        PW=Productos2Woocommerce()
        res= PW.sincronizar(id)#comentar para probar
        updateEstado(id,8)
        updateH(id,idas,idfa,8)
        if res["error"]==False:
            messages.success(request,  str(res['mensaje']))

    pr=Detalle_importacion.objects.filter(importacion=id)
        
        
    proveedores=Factura_proveedor.objects.filter(importacion=id)
    mercancias=Mercancia.objects.select_related().all()
    datos={
            "id":id,
            "idas":idas,
            "idfa":idfa,
            'error':False,
        "productos":pr,
    
        "proveedores":proveedores,
        "mercancias":mercancias
    }

    return render(request, 'core/resultados.html',datos  )

def buscarProductos(request,id,idas,idfa):#Recoge los sku ingresados en el formulario
    if request.method == 'POST':
        list_sku = request.POST.get('skus')
        productos=buscarSKU(list_sku,id,idas)#llamada al metodo de busqueda
        desha=""
        if(productos['error']==True):
            messages.success(request, 'No se ha encontado '+ str(productos['mensage']))
            if(len(productos['productos'])==0):
                
                desha="disabled"   
        datos={
                "id":id,
                "idas":idas,
                "idfa":idfa,
                "desha":desha
        }
        productos.update(datos)
    return render(request, 'core/preview_productos.html',productos ) 
        
def buscarSKU(skus,id,idas):#Cucion que realiza busqueda de los productos por sku
    sku=skus.split(';')
    pr =[] 
    provedor_prod=[]
    skuNoexist=[]
    result=np.unique(sku) 
    print(result) 
    for i in  range(len(result)): 

        if Producto.objects.filter(sku=result[i]).exists():  
            p = Producto.objects.get(sku=result[i])
            pr.append(p)
            estado=False
        else:
            print("No existe el sku ", result[i])
            skuNoexist.append(result[i])
            estado=True
    proveedores=Factura_proveedor.objects.filter(importacion=id)
    mercancias=Mercancia.objects.select_related().all()
    return {'error':estado,
            "mensage":skuNoexist,
            "productos":pr,
            "pr_p":provedor_prod,
            "proveedores":proveedores,
            "mercancias":mercancias }


def guardarProductoImport(sku,ide): 
    das=Das.objects.get(importacion=ide)
    imp=Importacion.objects.get(id=ide)
    fp=Factura_proveedor.objects.last()
    print(fp.proveedor)
    print(fp.proveedor.id)
    prove=Proveedor.objects.get(id=fp.proveedor.id)
    print("provedor",prove)
    di1=Detalle_importacion.objects.filter(importacion=ide).first()
    if(di1!=None):
        di=Detalle_importacion.objects.filter(importacion=ide)
        pim=[]
        for i in  range(len(di)):
            pim.append(di[i].producto.sku)
        indices = sku
        ind1 = pim
        ind2 = [x for x in indices if x not in ind1]
        print("s ku encontado", ind2)
        if(len(ind2)!=0):
            print(ind2)
            for i in  range(len(ind2)):
                p = Producto.objects.get(sku=ind2[i])
                mercan=Mercancia.objects.get(id=p.mercancia.id)
                dtp=Detalle_importacion(producto=p,das=das,importacion=imp, mercancia=mercan,proveedor=prove,valor_unitario=p.precio_compra)
                dtp.save()
    else:
        for i in  range(len(sku)):  
            p = Producto.objects.get(sku=sku[i])
            mercan=Mercancia.objects.get(id=p.mercancia.id)            
            dtp=Detalle_importacion(producto=p,das=das,importacion=imp, mercancia=mercan,proveedor=prove,valor_unitario=p.precio_compra)
            dtp.save()
                
    return 1    
    
def saveDetalleImportacion(ide,id_df,peso=[],precio=[],cantidad=[],id_prod=[],mercancia=[],proveedor=[],subtotal=[],advalorem=[],fodinfa=[],iva=[],ps=[],pr=[],prT=[],costo1=[],costo2=[],costo3=[], costo_unitario=[], inc_porcentual=[], inc_dolares=[]):
    das=Das.objects.get(importacion=ide)
    imp=Importacion.objects.get(id=ide)
    fp=Factura_proveedor.objects.last()
    for i in range(len(id_prod)):
        dtImport=Detalle_importacion()
        dtImport.id=id_df[i]
        dtImport.producto=Producto.objects.get(id=id_prod[i])
        dtImport.das=das
        dtImport.importacion=imp
        dtImport.mercancia=Mercancia.objects.get(id=mercancia[i])
        dtImport.proveedor=Proveedor.objects.get(id=proveedor[i])
        dtImport.valor_unitario=precio[i]
        dtImport.cantidad=cantidad[i]
        dtImport.peso=peso[i]
        dtImport.subtotal2=subtotal[i]
        dtImport.advalorem2=advalorem[i]
        dtImport.fodinfa2=fodinfa[i]
        dtImport.iva2=iva[i]
        dtImport.ps=ps[i]
        dtImport.pr=pr[i]
        dtImport.prt=prT[i]
        dtImport.costo1=costo1[i]
        dtImport.costo2=costo2[i]
        dtImport.costo3=costo3[i]
        dtImport.costo_unitario=costo_unitario[i]
        dtImport.inc_porcentual=inc_porcentual[i]
        dtImport.inc_dolares=inc_dolares[i]
        dtImport.save()
    return {'error':False}    