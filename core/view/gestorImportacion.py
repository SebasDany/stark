from core.view.gestorDas import updateSubtotal1
from core.sincronizacion import Productos2Woocommerce
from core.models import Das, Detalle_das, Detalle_importacion, Factura_proveedor, Importacion, Mercancia, Producto, Proveedor, Proveedor_producto
from ..controlador import  aranceles, costo_unitario, costos, incrementos, porcentuales, subtotal1, subtotal2, updateEstado, updateH
from django.shortcuts import render, redirect
import numpy as np 
from django.contrib import messages 
import datetime
import django_excel as excel

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
        sk_prove=request.POST.getlist('sk_prove')
        nombreProve=request.POST.getlist('nombreProve')
        
        mercancia=request.POST.getlist('mercancia')
        peso=request.POST.getlist('peso')
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,sk_prove,nombreProve)
        sub2=subtotal2(id)
        print("id_df id \t \t",id_df)
        updateSubtotal2(sub2["producto_id"],sub2["Subtotales2"])
        print("subtotal2 id \t \t",sub2["Subtotales2"])
        subt1=subtotal1(id)
        print("subtotal2 id \t \t",subt1["sub1_merc_t"])
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
        print("Subtotal",sub2["SumaSub2"], subt1["suma_sub1"])
        print("AranceL AD",arancel["suma_ad"], subt1["ad_das"], arancel["advalorem"])
        print("Fodinfa",arancel["suma_fod"], subt1["fod_das"], arancel["fodinfa"])
        if(sub2["SumaSub2"]!=subt1["suma_sub1"]):
            
            messages.error(request, "Validación INCORRECTA de suma de subtotales. Revisar los datos")
            return redirect('viewproduct',id,idas,idfa)
        if(arancel["suma_ad"]!=subt1["ad_das"]):
                
                messages.error(request, "Validación INCORRECTA de suma de Advalorem. Revisar los datos")
                return redirect('viewproduct',id,idas,idfa)
                
        if(arancel["suma_fod"]!=subt1["fod_das"]):
                print("ArancelFod",arancel["suma_fod"], subt1["fod_das"])
                messages.error(request, "Validación INCORRECTA de suma de Fodinfa. Revisar los datos")
                return redirect('viewproduct',id,idas,idfa)
        if(arancel["suma_iva"]!=subt1["iva_das"]):
                messages.error(request, "Validación INCORRECTA de suma de Iva. Revisar los datos")
                return redirect('viewproduct',id,idas,idfa)

        if(sub2["SumaSub2"]==subt1["suma_sub1"] and arancel["suma_ad"]==subt1["ad_das"] and arancel["suma_fod"]==subt1["fod_das"] and arancel["suma_iva"]==subt1["iva_das"] ):
            messages.success(request, "Validación correcta ")
            updateEstado(id,7)
            updateH(id,idas,idfa,7)
            return redirect( 'viewresults',id,idas,idfa )
       
       

    return 1



def viewResults(request,id,idas,idfa):# get per mite viszualizar los calculos realizados de la importacion y cuando es un post extrae los datos de catidad y costo_unitario de la base y de la tienda
    if request.method=='POST':
        PW=Productos2Woocommerce()
        PW.extraerDatosBase(id)
        d_tienda=PW.extraerDatosTienda(id)
        if d_tienda["error"]==False:
            if len(d_tienda["no_encontrado"])!=0:
                messages.error(request, "No se encontraron SKU "+ str(d_tienda["no_encontrado"])+"  en la tienda ")
            else:
                messages.error(request, "Se han encontrado todos los SKU ")
            PW.calcular(id)
        updateEstado(id,8)
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

    if request.method=='POST': #Realiza la sincronizacion con la tienda
        if "id_producto" in request.POST:
            ids=request.POST.getlist('id_producto')
            PW=Productos2Woocommerce()
            resp=PW.sincronizar(id)#sincroniza y actualiza los producto de la tienda
            if resp["error"]==False:
                messages.error(request,resp["mensaje"] )
                return redirect('updatetienda',id) 
    pr=Detalle_importacion.objects.filter(importacion=id)

    datos={ "id":id,
            "idfa":idfa,
            "idas":idas ,
            "productos":pr}

    updateH(id,idas,idfa,8)
    return render(request, 'core/preview_syncronizar.html',datos ) 

def updateTienda(request,id):
    if request.method == 'POST':
        print("estoy dentro del update ", id)
        listresults(id)
        return redirect('home')

    pr=Detalle_importacion.objects.filter(importacion=id)
    datos={"id":id,
    "productos":pr
    }
    
    
    return render (request, 'core/resultado_syncronizacion.html', datos) 
   


    
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

            provproduct=Proveedor_producto(producto=p,proveedor=prove,nombre="---")
            provproduct.save()
                
    return 1    
    
def saveDetalleImportacion(ide,id_df,peso=[],precio=[],cantidad=[],id_prod=[],mercancia=[],proveedor=[],skut=[],nombreT=[] ):
    das=Das.objects.get(importacion=ide)
    imp=Importacion.objects.get(id=ide)
    fp=Factura_proveedor.objects.last()
    #dtImport=Detalle_importacion()
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
        dtImport.save()
        updateProveedorProducto(id_prod[i],dtImport.proveedor,skut[i],nombreT[i],precio[i],peso[i],cantidad[i])
    return {'error':False} 

def updateProveedorProducto(idPro,prov,skut,nombreT,pre,pes,can):
    pP=Proveedor_producto.objects.filter(producto=idPro)
    print(pP[0].id)
    Proveedor_producto.objects.filter(id=pP[0].id).update(proveedor=prov, sku=skut,nombre=nombreT,precio=pre,peso=pes,cantidad=can)
    



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



def listresults(request,id):
    export = []
    # Se agregan los encabezados de las columnas
    export.append([
        'SKU','Nombre','Id producto tienda', 'Variacion ','Nuevo costo','Total inventario',"Fecha","Actualizado"
    ])
    # Se obtienen los datos de la tabla o model y se agregan al array
    results = Detalle_importacion.objects.filter(importacion=id)
    for result in results:
        # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
        # acceder a campos con relaciones y no solo al id
        export.append([result.producto.sku,
                        result.producto.nombre,
                        result.producto.id_woocommerce,
                        result.producto.variacion,
                        result.nuevo_costo,
                        result.total_inventario,
                        "{0:%Y-%m-%d %H:%M}".format(result.importacion.fecha),
                        result.actualizado,
                
                
                ])

    # Obtenemos la fecha para agregarla al nombre del archivo
    today    = datetime.datetime.today()
    strToday = today.strftime("%Y%m%d")

    # se transforma el array a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(export)

    # se devuelve como "Response" el archivo para que se pueda "guardar"
    # en el navegador, es decir como hacer un "Download"
    return excel.make_response(sheet, "csv", file_name="results-"+strToday+".csv")