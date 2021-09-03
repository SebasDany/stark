from core.view.gestorDas import updateSubtotal1
from core.sincronizacion import Sincronizacion
from core.models import Das, Detalle_das, Detalle_importacion, Factura_proveedor, Importacion, Mercancia, Producto, Proveedor, Proveedor_producto,Factura_afianzado,Detalle_afianzado
from ..utilidades import  updateEstado, updateH
from django.shortcuts import render, redirect
import numpy as np 
from django.contrib import messages 
import datetime
import django_excel as excel


#Muestra la pantalla de busqueda mediante el sku
def detalleImportacion(request,id,idas,idfa):
    datos={ "id":id,
            "idfa":idfa,
            "idas":idas }
    return render(request,'core/detalle_importacion.html',datos)
 
def addProductImport(request,id,idas,idfa):#guarda los productos importados en la base
    if request.method=='POST':
        if "id_producto" in request.POST:#
            sku=request.POST.getlist('id_producto')
            guardarProductoImport(sku,id)#llama al metodo con parametros sku=ides de los productos, id=ide de la importacion, para guardar los productos encontrados en la tabla detalle importacion
            updateEstado(id,6)#actualizamos el estado en el que se encuentra
            updateH(id,idas,idfa,6)#actualizamos la tabla historial para el dashborad
    return redirect('viewproduct',id,idas,idfa)#llamad a metodo viewProduct

def viewProduct(request,id,idas,idfa):#vista de los producto importadosde de la base
    pr=Detalle_importacion.objects.filter(importacion=id).order_by('id')
    # for i in Detalle_importacion.objects.filter(importacion=id):
    #     print("id",i.id)
    proveedores=Factura_proveedor.objects.filter(importacion=id).distinct()#obtien valores unicos de la factuarproveedor para mostrar los proveedores ingresados en esta tabla
    mercancias=Detalle_das.objects.filter(das=idas)#obtiene las mercancias ingresadas en detalle das
    datos={
                "id":id,
                "idas":idas,
                "idfa":idfa,
                'error':False,
                "productos_detalle_importacion":pr,
                "proveedores":proveedores,
                "mercancias":mercancias
            }
    return render(request, 'core/crear_importacion.html', datos ) #retona a la pagina de los productos de la importacion p
#permite actulizar los datos de los productos importados y procede a realizar todo el calculo
def productosImportados(request,id,idas,idfa):
    if request.method=='POST':
        
        product_id=request.POST.getlist('id_producto')  
        id_df=request.POST.getlist('id_df') 
        precio=request.POST.getlist('precio')
        proveedor=request.POST.getlist('proveedor')
        cantidad=request.POST.getlist('cantidad')
        sk_prove=request.POST.getlist('sk_prove')
        nombreProve=request.POST.getlist('nombreProve')
        
        mercancia=request.POST.getlist('mercancia')
        peso=request.POST.getlist('peso')
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,sk_prove,nombreProve)#Guarda o edita los datos de los productos de importacion
        updateMercanciaProducto(product_id,mercancia)#permita actualizar las mercancias en la tabla de los producto
        sub2=calcularSubtotal2(id)#llamada al metodo para caluclar el subtotal2
        ##print("id_df id \t \t",id_df)
        updateSubtotal2(sub2["producto_id"],sub2["Subtotales2"])#permite actualizar el subtotal en la tabla detalle importacion
        #print("subtotal2 id \t \t",sub2["Subtotales2"])
        subt1=cacularSubtotal1(id)#llamada la metodo para calcular el subtotal1 
        #print("subtotal2 id \t \t",subt1["sub1_merc_t"])
        updateSubtotal1(subt1["id_dd"],subt1["sub1_merc_t"])#permite actualizar el subtotal de la tabla detalle das
        arancel=calcularAranceles(id)#llamad al metodo para calcular los aranceles
        updateAranceles(arancel["producto_id"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"])#permite actualizar los aranceles en la tabla detalle importacion
        #print("arancel id \t \t",arancel["producto_id"])
        porcent=calcularPorcentuales(id)#llamada al metodo para el calculo de los porcentuales 
        updatePorcentuales(porcent["producto_id"],porcent["ps"],porcent["pr"],porcent["prT"])#actualiza los porcentuales en la tabla detalle importacion
        #print("porcent total id \t",porcent["producto_id"])
        costo=calcularCostos(id)#llamada al metodo para cacular los costos
        updateCostos(costo["producto_id"],costo["costo1"],costo["costo2"],costo["costo3"])#pemrite actulaizar los costos en la tabla detalle importacion
        #print("costo id \t \t",costo["producto_id"])
        costo_unit=calcularCosto_unitario(id)#llamada al metodo para calcular los costos unitarios
        updateCostoUnitario(costo_unit["producto_id"],costo_unit["costo1_unitario"])#permite actualizar los costos untarios en la tabla detalle importacion
        #print("costo_unit id \t \t",costo_unit["producto_id"])
        incremento=calcularIncrementos(id)#llamada la metodo para calcular los incrementos
        updateIncrementos(incremento["producto_id"], incremento["inc_porcentual"],incremento["inc_dolares"])#permite actualizar los incrementos en la tabla detalle importacion
        #print("incremento id \t \t",incremento["producto_id"])
        #print("Subtotal",sub2["SumaSub2"], subt1["suma_sub1"])
        #print("AranceL AD",arancel["suma_ad"], subt1["ad_das"], arancel["advalorem"])
        #print("Advalorem",round(arancel["suma_ad"],4), round(subt1["ad_das"],4))
        prTvalidacion=[]
        for i in Detalle_importacion.objects.values('proveedor').filter(importacion=id).distinct():#obtiene los proveedores unicos de la importacion
            acum=0
            for val  in Detalle_importacion.objects.filter(importacion=id).order_by('proveedor'):#obtiene los productos de la impotacion realizada 
                #print(i.get('proveedor'), val.proveedor.id )
                #print(i.get('proveedor')==val.proveedor.id)
                if(i.get('proveedor')==val.proveedor.id):#compara los provvedores para sumar el valor del prt
                    acum+=val.prt
            #print("sin rendondear", float(acum))
            #print("sin ", acum>=float(0.9998))
            if(float(acum)>=float(0.9998)):
                prTvalidacion.append(1)
            else:
                prTvalidacion.append(acum)#agrega el valor total encontado por cada tienda 
        valido=np.unique(prTvalidacion)
        if len(valido)!=1 or valido[0]!=1 :#verifica si el prt es distinto a 1 de ser asi manda el mensaje de error
            messages.error(request, "Validación INCORRECTA del prT. Revisar asignación de proveedores")
            return redirect('viewproduct',id,idas,idfa) #regresa a la vista de los prodcuto importados  

        if(sub2["SumaSub2"]!=subt1["suma_sub1"]):#verfifica que las sumas de los subtorales de la rabla general y del detalle das sean iguales
            
            messages.error(request, "Validación INCORRECTA de suma de subtotales. Revisar los datos")
            return redirect('viewproduct',id,idas,idfa)
        if(round(arancel["suma_ad"],4)!=round(subt1["ad_das"],4)):#verifica que los arance advalorem sean iguales de la tabla general y del detalle das
                messages.error(request, "Validación INCORRECTA de suma de Advalorem. Revisar mercancias")
                return redirect('viewproduct',id,idas,idfa)
        #print("ArancelFod",arancel["suma_fod"], subt1["fod_das"])
        if(round(arancel["suma_fod"],4)!=round(subt1["fod_das"],4)):#verifica que los arance fodinfa sean iguales de la tabla general y del detalle das
                ##print("ArancelFod",arancel["suma_fod"], subt1["fod_das"])
                messages.error(request, "Validación INCORRECTA de suma de Fodinfa. Revisar mercancías")
                return redirect('viewproduct',id,idas,idfa)
        if(float(round(arancel["suma_iva"],4))!=float(round(subt1["iva_das"],4))):#verifica que los arance iva sean iguales de la tabla general y del detalle das
                messages.error(request, "Validación INCORRECTA de suma de Iva. Revisar mercancías")
               # print("ArancelIVA",arancel["suma_iva"],subt1["iva_das"])
                return redirect('viewproduct',id,idas,idfa)
        #vericica que todas las validaciosn enates mecionadas sena correctas se ser asi muestra el resultado de los calculos
        if(sub2["SumaSub2"]==subt1["suma_sub1"] and round(arancel["suma_ad"],4)==round(subt1["ad_das"],4)and round(arancel["suma_fod"],4)==round(subt1["fod_das"],4) and round(arancel["suma_iva"],4)==round(subt1["iva_das"],4 )):
            messages.success(request, "Validación correcta ")
            updateEstado(id,7)#actualiza el esto de la importacion
            updateH(id,idas,idfa,7)#actualiza el la taba historial
            return redirect( 'viewresults',id,idas,idfa )#redirige a la vista de los resultados
       
       

    return 1


#metodo get permite viszualizar los calculos realizados de la importacion, cuando es un post extrae los datos de catidad y costo_unitario de la base y de la tienda
def viewResults(request,id,idas,idfa):
    if request.method=='POST':
        PW=Sincronizacion() #instanciacion de la clase sincronizacion
        PW.extraerDatosBase(id)#llamda el metodo para extraer los datos como cantidad y costo_unitario de la base
        d_tienda=PW.extraerDatosTienda(id)#llamda el metodo para extraer los datos como stoc_cuantity y purchase_price de la tienda
        if d_tienda["error"]==False:#manda un mensaje si algun producto no s eha encontrado en la tienda
            if len(d_tienda["no_encontrado"])!=0:
                messages.error(request, "No se encontraron SKU "+ str(d_tienda["no_encontrado"])+"  en la tienda ")
            else:
                messages.error(request, "Se han encontrado todos los SKU ")
            PW.calcular(id)#llamada al metodo para calcular el nuevo costo y el nuevo inventario
        if d_tienda["error1"]==True:
            messages.error(request, "No se ha podido conectar a la tienda error autenticacion")
            pr=Detalle_importacion.objects.filter(importacion=id) #obtiene los productos de una importacion   
            proveedores=Factura_proveedor.objects.filter(importacion=id)
            mercancias=Mercancia.objects.select_related().all()
            datos={
                    "id":id,
                    "idas":idas,
                    "idfa":idfa,
                    'error':False,
                "productos":pr,
                "tipoerror":"alert alert-danger",
                "proveedores":proveedores,
                "mercancias":mercancias
            } 
            return render(request, 'core/resultados.html',datos  )

        updateEstado(id,8)#actulaiza el estado de la importacion
        updateH(id,idas,idfa,8)
        return redirect('previewsyncronizar',id,idas,idfa )#redirige a la vista de previzualizacion para la altualizacion en la tirnda 
    pr=Detalle_importacion.objects.filter(importacion=id)    
    proveedores=Factura_proveedor.objects.filter(importacion=id)
    mercancias=Mercancia.objects.select_related().all()
    datos={
            "id":id,
            "idas":idas,
            "idfa":idfa,
            'error':False,
            "tipoerror":"alert alert-success",
        "productos":pr,
        "proveedores":proveedores,
        "mercancias":mercancias
    } 
    return render(request, 'core/resultados.html',datos  )

def previewSyncronizar(request,id,idas,idfa):#permite previzulizar los datos a sincronyzar

    if request.method=='POST': #Realiza la sincronizacion con la tienda
        if "id_producto" in request.POST:
            ids=request.POST.getlist('id_producto')
            PW=Sincronizacion()#instancia de la clase sincronizacion
            resp=PW.sincronizar(id)#sincroniza y actualiza los producto de la tienda
            if resp["error"]==False:#responde erro false si realizo la sincronizacion
                messages.success(request,resp["mensaje"] )
                updateEstado(id,9)#actualizacion del estado dela importacion
                updateH(id,idas,idfa,9)#actualizacion del estado del historial
                return redirect('updatetienda',id) #retorna a la vizaulizacion de los productos ya sincronizados
    pr=Detalle_importacion.objects.filter(importacion=id)

    datos={ "id":id,
            "idfa":idfa,
            "idas":idas ,
            "productos":pr}

    
    return render(request, 'core/preview_syncronizar.html',datos ) 

def updateTienda(request,id):#vista de resultado de la sincronizacion realizada
    

    pr=Detalle_importacion.objects.filter(importacion=id)
    datos={"id":id,
    "productos":pr
    }
    
    
    return render (request, 'core/resultado_syncronizacion.html', datos) 
   


#Recoge los sku ingresados en del formulario detalle_Iportacion.html    
def buscarProductos(request,id,idas,idfa):
    if request.method == 'POST':
        list_sku = request.POST.get('skus')
        productos=buscarSKU(list_sku,id,idas)#llamada al metodo de busqueda de los productos d el base de datos
        desha=""
        tipoMess=""
        if(productos['error']==False):#retorna un errro como falso si encuentra todos los productos
            messages.success(request, 'Se han encontrado todos los sku ')
            tipoMess="alert alert-success alert-dismissable"
        if(productos['error']==True):# retorna un erro cono true si algun producto no se ha encontrado
            messages.error(request, 'No se ha encontrado '+str(productos['mensage']))
            tipoMess="alert alert-danger alert-dismissable"
            if(len(productos['productos'])==0):#si el tamaño encontrado de los productos esi gual a cero manda deshabiltar le boton
                
                desha="disabled"   #estado de l boton siguiente
        datos={
                "id":id,
                "idas":idas,
                "idfa":idfa,
                "desha":desha,
                "tipoMess":tipoMess
                
        }
        productos.update(datos)#añade datos a la respuesta del metodo buscarSKU 
        return render(request, 'core/preview_productos.html',productos )#retorna los producto para la previzualizacion 
    datos={ "id":id,
            "idfa":idfa,
            "idas":idas }
    return render(request,'core/detalle_importacion.html',datos)
# realiza busqueda de los productos por sku dentro de la base de datos       
def buscarSKU(skus,id,idas):
    sku=skus.split(';')#separa los sku enviados al encontrar el " ; "
    pr =[] 
    provedor_prod=[]
    skuNoexist=[]
    result=np.unique(sku) #Obtine unicos sku
    estado=False
    for i in  range(len(result)): 

        if Producto.objects.filter(sku=result[i]).exists():# si el producto con el sku existe se agrega al vector de pr
            p = Producto.objects.get(sku=result[i])
            pr.append(p)#agrega el producto encontrado
            
        else:
            skuNoexist.append(result[i])#si no se encuentra el producto agrega el sku 
            estado=True#cambio de stado a true si no encuentra algun producto
    proveedores=Factura_proveedor.objects.filter(importacion=id)
    mercancias=Mercancia.objects.select_related().all()
    return {'error':estado,
            "mensage":skuNoexist,
            "productos":pr,
            "pr_p":provedor_prod,
            "proveedores":proveedores,
            "mercancias":mercancias }

#permite guardar los productos encontrado en la busqueda
def guardarProductoImport(sku,ide): 
    das=Das.objects.get(importacion=ide)#obtiene el objeto DAS de la importacion actual
    imp=Importacion.objects.get(id=ide)#obtiene el objeto de la importacion que se esta realizando
    fp=Factura_proveedor.objects.last()
    prove=Proveedor.objects.get(id=fp.proveedor.id)
    di1=Detalle_importacion.objects.filter(importacion=ide).first()#obtien el primer registro para validar si cea creado ya no volver a crear
    if(di1!=None):
        di=Detalle_importacion.objects.filter(importacion=ide)
        pim=[]
        for i in  range(len(di)):
            pim.append(di[i].producto.sku)
        indices = sku
        ind1 = pim
        ind2 = [x for x in indices if x not in ind1]#permite verificar si no existe esse sku creado si existe alguno creo lo que los que no existen
        if(len(ind2)!=0):#solo permite crear los productos faltantes dentro de esta importacion
            for i in  range(len(ind2)):
                p = Producto.objects.get(sku=ind2[i])
                mercan=Mercancia.objects.get(id=p.mercancia.id)
                dtp=Detalle_importacion(producto=p,das=das,importacion=imp, mercancia=mercan,proveedor=prove,valor_unitario=p.precio_compra)
                dtp.save()
    else:#guarda todos los productos en la tabla detalle importacion
        for i in  range(len(sku)):  
            p = Producto.objects.get(sku=sku[i])
            mercan=Mercancia.objects.get(id=p.mercancia.id)            
            dtp=Detalle_importacion(producto=p,das=das,importacion=imp, mercancia=mercan,proveedor=prove,valor_unitario=p.precio_compra)
            dtp.save()

            provproduct=Proveedor_producto(producto=p,proveedor=prove,nombre="---")
            provproduct.save()
                
    return 1    
 #Guarda todos los datos de los productos modificados o ingresados en la tabla detalle importacicon   
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
        
        if(len(skut[i]) >0 or len(nombreT[i])>0 ):
            updateProveedorProducto(id_prod[i],dtImport.proveedor,skut[i],nombreT[i],precio[i],peso[i],cantidad[i])#Permite actualizar la tabla productoproveedor
    return {'error':False} 

#permite extraer los datos de la tabla detalle afianzado
def tablaAfianzado(id_imp):
    ##importacion_afianzado
    imp = Importacion.objects.get(id=id_imp)
    factur=Factura_afianzado.objects.get(importacion=imp.id)
    precios=[]
    peso=[]
    iva=[]
    for valores in Detalle_afianzado.objects.filter(factura_afianzado=factur.id):
        precios.append(valores.al_precio)#añade los datos aun vector
        peso.append(valores.al_peso)
        iva.append(valores.iva)
    sum_precios=sum(precios)#realiza la suma de los datos 
    sum_peso=sum(peso)
    sum_iva=sum(iva)
    datos={"sum_precios": sum_precios,
        "sum_peso": sum_peso,
        "sum_iva": sum_iva
        }
    return  datos


def validacion(subt1,subt2):
    #Si es igual me devuelve 1 sino me devuelve un cero
    if subt1==subt2:
        var=1
    else:
        var=0   
    return  var


#realiza el calculo del subtotal de la tabla general
def calcularSubtotal2(id_imp):
    ##Suma de subtotal2
    imp = Importacion.objects.get(id=id_imp)
    # print("impresp",imp.id)
    sub2_pro=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=id_imp):
        sub2_pro.append(valores.cantidad*valores.valor_unitario)#agrega a un array el valor de cantidad por el costo
        producto_id.append(valores.id)
    
    # saveDetalleImportacion
    suma_subt2=sum(sub2_pro)
    datos={"producto_id": producto_id,
    "Subtotales2": sub2_pro,
    "SumaSub2": suma_subt2
    }
    return datos
#pemite calcular el subtotal del la tabla detalle das
def cacularSubtotal1(id_imp):
    ##Suma de subtotal1
    imp = Importacion.objects.get(id=id_imp)
    das_imp=Das.objects.get(importacion=imp)#obtiene el objeto de la tabla das de la importacion actual
    sub1_merc_t=[]
    id_dd=[]
    ad_das=0
    fod_das=0
    iva_das=0
    for valores in Detalle_das.objects.filter(das=das_imp):#obtiene los objetos del detalle das deacuerdo al das
        acum=0 
        ad_das+=valores.advalorem1#acumumula los datos obtenidos del tabla detalle das
        fod_das+=valores.fodinfa1
        iva_das+=valores.iva1
        for valor in Detalle_importacion.objects.filter(importacion=id_imp):
            if valores.mercancia==valor.mercancia:#obtine el subtotal de acuerdo a las mercancias para actualizar en el detalle das 
                #sub1_merc.append(valores.subtotal1)
                acum+=valor.subtotal2 #acumula el subtotal por cada tipo de mercancia
                
        sub1_merc_t.append(acum)#añade dentro del vector el subtotal dpor cada tipo de mercancia
        suma_sub1=sum(sub1_merc_t)
        id_dd.append(valores.id)
    datos={ "sub1_merc_t":sub1_merc_t,
                "id_dd":id_dd,
                "suma_sub1": suma_sub1,
                "ad_das": ad_das,
                "fod_das": fod_das,
                "iva_das": iva_das
        }
    # print("factura id",extra_tienda)
    return  datos
#carcula los aranceles para la tabla general
def calcularAranceles(id_imp):
    #Calculos de advalorem, fodinfa e iva
    imp = Importacion.objects.get(id=id_imp)#obtiene el objeto de la importacion correspondiente  al id de la importacion
    das_imp=Das.objects.get(importacion=imp)#obtiene el objeto das de la importacion actual
    advalorem=[]
    fodinfa=[]
    iva=[]
    producto_id=[]
    for valor in Detalle_das.objects.filter(das=das_imp):#realiza la busqueda de todas mercancias ingresadas de una importacion especifica
        tam=0
        var=Detalle_importacion.objects.filter(mercancia=valor.mercancia.id , importacion = id_imp)#obtiene objetos donde se igual a la mercancia del detalle das y que sea de la importacion actual
        tam=len(var)#obtenermos el tamaño del producto encontrado para esa mercancia
        #print("mercancia", valor.mercancia, "id ", valor.mercancia.id )
        for valores in Detalle_importacion.objects.filter(importacion=imp.id):#obtiene los objetos de la importacion actual de la tabla detalle importacion
            #print("Mercancia",valor.mercancia,"id", valor.mercancia.id,"id DAS",valores.mercancia.id, " Tamaño", tam, " ", valores.mercancia.id==valor.mercancia.id) 
            
            if valores.mercancia.id==valor.mercancia.id:#compara si la mercacia del detalledas sea igual con los del detalleimportacion
                
                producto_id.append(valores.id)#agrega a un vector el id del objeto de que coincida con la mercancia de detalledas
                if tam==1:#si el tamaño de los producto es igual a 1 no se realizada ningun calculo
                    advalorem.append(valor.advalorem1)#se agrega directamente el valor del advalorem 
                    fodinfa.append(valor.fodinfa1)#se agrega directamente el valor del fodinfa
                    iva.append(valor.iva1)#se agrega directamente el valor del iva
                   # print("mercancia", valores.mercancia, "tamaño", tam, valores.subtotal2, valor.subtotal1)
                    #print("-------------",valores.producto.sku," ",valor.mercancia, " ", (valores.subtotal2/valor.subtotal1)*valor.fodinfa1, valores.subtotal2,valor.subtotal1, valor.fodinfa1)
                else:
                    if valor.advalorem1==0:#si el advalorem es cero este va directamente con cero solo se calcula el fordinfa y el iva
                        advalorem.append(0)
                        fodinfa.append((valores.subtotal2/valor.subtotal1)*valor.fodinfa1)
                        iva.append((valores.subtotal2/valor.subtotal1)*valor.iva1)
                        #print("-------------",valores.producto.sku," ",valor.mercancia, " ",(valores.subtotal2/valor.subtotal1)*valor.fodinfa1, valores.subtotal2,valor.subtotal1, valor.fodinfa1)
                        #print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.fodinfa1 ," ",(valores.subtotal2/valor.subtotal1)*valor.fodinfa1) 
                    if valor.fodinfa1==0:#si el fodinfa es cero este va directamente con cero solo se calcula el advalorem y el iva
                        fodinfa.append(0)
                        advalorem.append((valores.subtotal2/valor.subtotal1)*valor.advalorem1)
                        iva.append((valores.subtotal2/valor.subtotal1)*valor.iva1)
                        #print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.fodinfa1 ," ", (valores.subtotal2/valor.subtotal1)*valor.fodinfa1) 
                        #print("-------------",valores.producto.sku," ",valor.mercancia, " ",(valores.subtotal2/valor.subtotal1)*valor.fodinfa1, valores.subtotal2,valor.subtotal1, valor.fodinfa1)
                    if valor.iva1==0: #si el iva es cero este va directamente con cero solo se calcula el fordinfa y el advalorem
                        advalorem.append((valores.subtotal2/valor.subtotal1)*valor.advalorem1)
                        fodinfa.append((valores.subtotal2/valor.subtotal1)*valor.fodinfa1)            
                        iva.append(0)
                        #print("-------------",valores.producto.sku," ",valor.mercancia, " ",(valores.subtotal2/valor.subtotal1)*valor.fodinfa1, valores.subtotal2,valor.subtotal1, valor.fodinfa1)
                        #print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.fodinfa1 ," ", (valores.subtotal2/valor.subtotal1)*valor.fodinfa1) 

                    if  valor.advalorem1!=0 and valor.fodinfa1!=0 and valor.iva1!=0 and tam>1:#mientars sea diferente a las condiciones anteriores se calcula todos los aranceles
                        advalorem.append((valores.subtotal2/valor.subtotal1)*valor.advalorem1)
                        fodinfa.append((valores.subtotal2/valor.subtotal1)*valor.fodinfa1)
                        iva.append((valores.subtotal2/valor.subtotal1)*valor.iva1)
                        #print("-------------",valores.producto.sku," ",valor.mercancia, " ",(valores.subtotal2/valor.subtotal1)*valor.fodinfa1, valores.subtotal2,valor.subtotal1, valor.fodinfa1)
                    # print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.fodinfa1 ," ", (valores.subtotal2/valor.subtotal1)*valor.fodinfa1) 
                        
    suma_ad=sum(advalorem)#suma total del advalorem
    suma_fod=sum(fodinfa)#suma total del fodinfa
    suma_iva=sum(iva)#suma total del iva
    datos={"producto_id": producto_id,
        "advalorem": advalorem,
        "fodinfa": fodinfa,
        "iva": iva,
        "suma_ad":suma_ad,
        "suma_fod":suma_fod,
        "suma_iva":suma_iva,
        }

    return datos

#realiza el calculo de los porcentuales recibe como parametro el ide de la importacion
def calcularPorcentuales(id_imp):
    pesos=[]
    ps=[]
    pr=[]
    prT=[]
    producto_id=[]
    for i in Detalle_importacion.objects.filter(importacion=id_imp): #obtine los objetos de la tabla detalleImportacion de la imprtacion actual
        pesos.append(i.peso)#se añade el peso dentro de un vector
    suma_peso=sum(pesos)#se suma los pesos del vector

    suma_subtotal2=calcularSubtotal2(id_imp)#llamda al metodo para obtener el subtotal2  
    for valor in Factura_proveedor.objects.filter(importacion=id_imp):
        for valores in Detalle_importacion.objects.filter(importacion=id_imp):

            if(valores.proveedor==valor.proveedor):#busqueda del proveedor dentro de la tabla detalle importacion
                prT.append(valores.subtotal2/valor.valor_factura)#calculo del pocentual prT
                ps.append(valores.peso/suma_peso)#calculo del porcentual del peso
                pr.append(valores.subtotal2/suma_subtotal2["SumaSub2"])#calculo del porcentual del precio
                producto_id.append(valores.id)#toma de los id de los objetos de la importacion
                #print("--------",valores.id, ps,pr,prT)
                

    datos={"producto_id": producto_id,
        "ps": ps,
        "pr": pr,
        "prT": prT
        }
    return  datos
#calculo de costos 
def calcularCostos(id_imp):
    tabla_afianz=tablaAfianzado(id_imp)
    costo1=[]
    costo2=[]
    costo3=[]
    producto_id=[]
    
    for valores in Detalle_importacion.objects.filter(importacion=id_imp):#busqueda de la objetos de la importacion actual
        for valor in Factura_proveedor.objects.filter(importacion=id_imp):
            if(valores.proveedor==valor.proveedor):#compara que los proveedores sean iguales
                costo1.append((tabla_afianz["sum_precios"]+tabla_afianz["sum_iva"])*valores.pr)#calculo del costo1
                costo2.append(tabla_afianz["sum_peso"]*valores.ps)#calculo del costo2
               # print("-----------",tabla_afianz["sum_peso"],valores.ps, tabla_afianz["sum_peso"]*valores.ps)
                producto_id.append(valores.id)
                costo3.append(valor.extra*valores.prt)#calculo del costo3
                
    datos={"producto_id": producto_id,
        "costo1": costo1,
        "costo2": costo2,
        "costo3": costo3
        }
    return  datos

#calculo del costo unitario 
def calcularCosto_unitario(id_imp):
    imp = Importacion.objects.get(id=id_imp)
    costo1_unitario=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        #calculo del costo unitario
        
        cu=valores.valor_unitario+((valores.advalorem2+valores.fodinfa2+valores.iva2+valores.costo1+valores.costo2+valores.costo3)/valores.cantidad)
        costo1_unitario.append(cu)
        producto_id.append(valores.id)
     
    datos={"producto_id": producto_id,
        "costo1_unitario": costo1_unitario
        }
    return  datos

#calcular incrementos
def calcularIncrementos(id_imp):
    imp = Importacion.objects.get(id=id_imp)
    inc_porcentual=[]
    inc_dolares=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):#obtien los objetos de la importacion actual
        producto_id.append(valores.id)
        #print(valores.costo_unitario,"-",valores.valor_unitario,"/",valores.valor_unitario)

        ip=(valores.costo_unitario-valores.valor_unitario)/valores.valor_unitario

        inc_porcentual.append(ip)#calculo del incremeto en porcentual
        inc_dolares.append(valores.costo_unitario-valores.valor_unitario)#calculo incremento en dolares
  
    datos={"producto_id": producto_id,
        "inc_porcentual": inc_porcentual,
        "inc_dolares": inc_dolares
        }
    return  datos

#actualiza datos en la tabla proveedor producto
def updateProveedorProducto(idPro,prov,skut,nombreT,pre,pes,can):
    pP=Proveedor_producto.objects.filter(producto=idPro)
    #print(pP[0].id)
    Proveedor_producto.objects.filter(id=pP[0].id).update(proveedor=prov, sku=skut,nombre=nombreT,precio=pre,peso=pes,cantidad=can)

def updateMercanciaProducto(id_pro, mercancia):#actualiza la mercancia en la tabla producto
    for i in range(len(id_pro)):
        Producto.objects.filter(id=id_pro[i]).update(mercancia=Mercancia.objects.get(id=mercancia[i])) 

def updateSubtotal2(id_dI, subt2):#actualiza el subtotal en la tabla detalle importacion
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(subtotal2=subt2[i])

#actualiza los aranceles en la tabla detalle importacion
def updateAranceles(id_dI,advalorem, fodinfa, iva):
    
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(advalorem2=advalorem[i],fodinfa2=fodinfa[i],iva2=iva[i])
    
def updatePorcentuales(id_dI,ps, pr, prT):#actualiza los porcentuales en la tabla detalle importacion
    for i in range(len(id_dI)):
        #print(ps[i],round(pr[i],4),prT[i])
        Detalle_importacion.objects.filter(id=id_dI[i]).update(ps=round(ps[i],4),pr=round(pr[i],4),prt=round(prT[i],4))

def updateCostos(id_dI,cost1,cost2, cost3):#actualiza costos en la tabla detalle importacion
    #print("el tamao es ",len(id_dI),len(cost1),len(cost2),len(cost3))
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(costo1=cost1[i],costo2=cost2[i],costo3=cost3[i])

def updateCostoUnitario(id_dI,cost_u):#actualiza costo unitario en la tabla detalle importacion
    for i in range(len(id_dI)):
        Detalle_importacion.objects.filter(id=id_dI[i]).update(costo_unitario=cost_u[i])

def updateIncrementos(id_dI,inc_porcen,inc_dol):#actualiza lo incrementos de la tabla detalleimportacion
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

def exportarCalculoImportacion(request,id):
    exportar = []
    # Se agregan los encabezados de las columnas
    exportar.append([
        'SKU','Proveedor','Nombre','ValorUnid','Cantidad','Subtotal','Mercancia','Peso','Advalorem','Fodinfa','Iva','Ps(%)','Pr(%)','PrT(%)','Costo1','Costo2','Costo3','C_Unit','INC(%)','INC($)'
    ])
    # Se obtienen los datos de la tabla o model y se agregan al array
    resultado = Detalle_importacion.objects.filter(importacion=id)
    for lista in resultado:
        print(lista.ps)
        # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
        # acceder a campos con relaciones y no solo al id
        exportar.append([lista.producto.sku,
            lista.proveedor.nombre,
            lista.producto.nombre,
            lista.valor_unitario,
            lista.cantidad,
            lista.subtotal2,
            lista.mercancia.nombre,
            lista.peso,
            lista.advalorem2,
            lista.fodinfa2,
            lista.iva2,
            lista.ps*100,
            lista.pr*100,
            lista.prt*100,
            lista.costo1,
            lista.costo2,
            lista.costo3,
            lista.costo_unitario,
            lista.inc_porcentual*100,
            lista.inc_dolares
                
                
                ])

    # Obtenemos la fecha para agregarla al nombre del archivo
    today    = datetime.datetime.today()
    strToday = today.strftime("%Y%m%d")

    # se transforma el array a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(exportar)

    # se devuelve como "Response" el archivo para que se pueda "guardar"
    # en el navegador, es decir como hacer un "Download"
    return excel.make_response(sheet, "csv", file_name="resultsImportacion-"+strToday+".csv")