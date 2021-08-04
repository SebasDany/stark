


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
                "productos_detalle_importacion":pr,
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
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor)
        subtotal=subtotal2(id)
        print("id_df id \t \t",id_df)
        
        updateSubtotal2(subtotal["producto_id"],subtotal["Subtotales2"])
        print("subtotal2 id \t \t",subtotal["producto_id"])
        subt1=subtotal1(id)
        updateSubtotal1(subt1["id_dd"],subt1["sub1_merc_t"])
        arancel=aranceles(id)
        updateAranceles(arancel["producto_id"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"])
        print("arancel id \t \t",arancel["producto_id"])
        porcent=porcentuales(id)
        updatePorcentuales(porcent["producto_id"],porcent["ps"],porcent["pr"],porcent["prT"])
        print("porcent total id \t",porcent["producto_id"])
        costo=costos(id)
        updateCostos(costo["producto_id"],costo["costo1"],costo["costo2"],costo["costo3"])
        print("costo id \t \t",costo["producto_id"])
        costo_unit=costo_unitario(id)
        updateCostoUnitario(costo_unit["producto_id"],costo_unit["costo1_unitario"])
        print("costo_unit id \t \t",costo_unit["producto_id"])
        incremento=incrementos(id)
        updateIncrementos(incremento["producto_id"], incremento["inc_porcentual"],incremento["inc_dolares"])
        print("incremento id \t \t",incremento["producto_id"])
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
        PW.extraerDatosBase(id)
        d_tienda=PW.extraerDatosTienda(id)
        if d_tienda["error"]==False:
            PW.calcular(id)
            messages.error(request, "Se han encontrado todos los SKU ")
        else:
            messages.error(request, "No se encontraron SKU "+ str(d_tienda["no_encontrado"]+"  en la tienda "))
            

        updateEstado(id,8)
        
        # if res["error"]==False:
        #     messages.success(request,  str(res['mensaje']))

        return redirect('previewsyncronizar',id,idas,idfa )

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

def previewSyncronizar(request,id,idas,idfa):#permite previzulizar los datos a sincronyzar

    
    pr=Detalle_importacion.objects.filter(importacion=id)

    datos={ "id":id,
            "idfa":idfa,
            "idas":idas ,
            "productos":pr}

    updateH(id,idas,idfa,8)

    return render(request, 'core/preview_syncronizar.html',datos ) 
def updateTienda(request,id):

    if request.method=='POST':
        if "id_producto" in request.POST:
            ids=request.POST.getlist('id_producto')
            PW=Productos2Woocommerce()
            resp=PW.sincronizar(id)
            if resp["error"]==False:
                messages.error(request,resp["mensaje"] )
                return render (request, 'core/resultado_syncronizacion.html') 

    
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
        ind2 = [x for x in indices if x not in ind1]#permite verificar si no existe esse sku creado si existe alguno creo lo que los que no existen
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
    
def saveDetalleImportacion(ide,id_df,peso=[],precio=[],cantidad=[],id_prod=[],mercancia=[],proveedor=[]):
    das=Das.objects.get(importacion=ide)
    imp=Importacion.objects.get(id=ide)
    fp=Factura_proveedor.objects3.last()
    dtImport=Detalle_importacion()
    for i in range(len(id_prod)):
        
        dtImport.id=id_df[i]
        dtImport.producto=Producto.objects.get(id=id_prod[i])
        dtImport.das=das
        dtImport.importacion=imp
        dtImport.mercancia=Mercancia.objects.get(id=mercancia[i])
        dtImport.proveedor=Proveedor.objects.get(id=proveedor[i])
        dtImport.valor_unitario=precio[i]
        dtImport.cantidad=cantidad[i]
        dtImport.peso=peso[i]
        dtImport.save()
    return {'error':False}    
def updateSubtotal2(id_dI, subt2):
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(subtotal2=subt2[i])


def updateAranceles(id_dI,advalorem, fodinfa, iva):
    
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(advalorem2=advalorem[i],fodinfa2=fodinfa[i],iva2=iva[i])
    
def updatePorcentuales(id_dI,ps, pr, prT):
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(ps=ps[i],pr=pr[i],prt=prT[i])

def updateCostos(id_dI,cost1,cost2, cost3):
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(costo1=cost1[i],costo2=cost2[i],costo3=cost3[i])

def updateCostoUnitario(id_dI,cost_u):
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(costo_unitario=cost_u[i])

def updateIncrementos(id_dI,inc_porcen,inc_dol):
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(inc_porcentual=inc_porcen[i],inc_dolares=inc_dol[i])

