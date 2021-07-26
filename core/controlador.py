


from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto

import numpy as np  

def buscarSKU(skus,id,idas):
    sku=skus.split(';')
    pr =[] 
    provedor_prod=[]
    result, indices=np.unique(sku,return_index=True) 
    print(result) 
    # print(result)  
    # print(indices ) 
    # print(sku[indices] )
    
    di1=Detalle_importacion.objects.filter(importacion=id).first()
    
    # if(di1!=None):
    #     di=Detalle_importacion.objects.filter(importacion=id)
    #     pim=[]
    #     for i in  range(len(di)):
    #         pim.append(di[i].producto.sku)
    #     indices = result
    #     ind1 = pim
    #     ind2 = [x for x in indices if x not in ind1]
    #     if(len(ind2)!=0):
    #         print(ind2)
    #         for i in  range(len(ind2)):
    #             p = Producto.objects.get(sku=ind2[i])
    #             mercan=Mercancia.objects.get(id=p.mercancia.id)
    #             dtp=Detalle_importacion(producto=p,das=das,importacion=imp, mercancia=mercan,proveedor=prove,valor_unitario=p.precio_compra)
    #             dtp.save()
    #             pr.append(p)
        #pr=Detalle_importacion.objects.filter(importacion=id)
        
    # else:

    for i in  range(len(result)):
            
        p = Producto.objects.get(sku=result[i])
        mercan=Mercancia.objects.get(id=p.mercancia.id)
        v=p.proveedor_producto_set.all()
        print("###################################",len(v))
        if(len(v)!=0):
            print(v[0].sku)
        
        
        # dtp=Detalle_importacion(producto=p,das=das,importacion=imp, mercancia=mercan,proveedor=prove,valor_unitario=p.precio_compra)
        # dtp.save()
        pr.append(p)
    #pr=Detalle_importacion.objects.filter(importacion=id)
            
            
        

    
    proveedores=Factura_proveedor.objects.filter(importacion=id)
    mercancias=Mercancia.objects.select_related().all()
    
    
    return {'error':False,
    "productos":pr,
    "pr_p":provedor_prod,
    "proveedores":proveedores,
    "mercancias":mercancias
  
           }

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

def saveDetalleImportacion(ide,id_df,peso=[],precio=[],cantidad=[],id_prod=[],mercancia=[],proveedor=[]):
    
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
        dtImport.save()
        print("################# hola estoy dentro saveDetalleImportacion")

    
    return {'error':False}    

def saveFacuturaProveedor(idfp,prove,id,ncajas,v_envio,v_factura,comis_envio,comis_tarjeta,isd,t_pago,extra):
    
    
    for j in range (len(prove)):
        
       
        fp = Factura_proveedor()
        
            #entero = int(posible_numero)
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

def saveDetalleDas(id_dd,idas,mercancia=[],advalorem=[],fodinfa=[],iva=[]):

    das=Das.objects.get(id=idas)# obtiene el utlimo dato del la consulta
    
    for i in  range(len(mercancia)):
        dD=Detalle_das()
        
        dD.mercancia=Mercancia.objects.get(id = mercancia[i])
        dD.das=das
        dD.advalorem1=advalorem[i]
        dD.fodinfa1=fodinfa[i]
        dD.iva1=iva[i]
        dD.id=id_dd[i]
        dD.save()
        print(i)

    return {'error':False}

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
def saveMercacia(mer=[],sub=[],adv=[]):
    print(len(mer))
    print(len(sub))
    print(len(adv))
    for i in range(len(mer)):
        print(mer[i])
        m=Mercancia()
        m.nombre=mer[i]
        m.subpartida=sub[i]
        m.por_advalorem=adv[i]
        m.save()
def saveProducto(mercancia=[],id_wo=[],sku=[],nombre=[],precio_compra=[],precio_neto=[],variacion =[],
parent_id=[],imagen=[],categorias=[],observaciones=[]):
    print(len(mercancia))
    print(len(nombre))
    print(len(sku))
    print(mercancia[0])

    for i in range(len(mercancia)):
        pr=Producto()
        pr.mercancia=Mercancia.objects.get(nombre=mercancia[i])
        pr.id_woocommerce=2
        pr.sku=sku[i]
        pr.nombre=nombre[i]
        pr.precio_compra=45.0
        pr.precio_neto=50.5
        pr.variacion=1
        pr.parent_id=3
        pr.imagen="djsfjdnjfndjn.jpg"
        pr.categorias=mercancia[i]
        pr.observaciones="descripcion del producto"
        pr.save()



def tablaAfianzado(id_imp):
    ##importacion_afianzado
    # print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    # print("impresp",imp.id)
    factur=Factura_afianzado.objects.get(importacion=imp.id)
    # print("factura id",factur.id)
    precios=[]
    peso=[]
    iva=[]
    for valores in Detalle_afianzado.objects.filter(factura_afianzado=factur.id):
        precios.append(valores.al_precio)
        peso.append(valores.al_peso)
        iva.append(valores.iva)
    sum_precios=sum(precios)
    sum_peso=sum(peso)
    sum_iva=sum(iva)
    # print("factura afianzado",sum(precios))
    # print("factura afianzado",sum(peso))
    # print("factura afianzado",sum(iva))
    return  [sum_precios, sum_peso, sum_iva]

def tablaProveedor(id_imp):
    ##importacion_proveedor
    print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    print("impresp",imp.id)
    subt_tienda=[]
    extra_tienda=[]
    for valores in Factura_proveedor.objects.filter(importacion=imp.id):
        subt_tienda.append(valores.valor_factura)
        extra_tienda.append(valores.extra)
    # print("factura id",subt_tienda)
    # print("factura id",extra_tienda)
    return  [subt_tienda, extra_tienda]

def subtotal2(id_imp):
    ##Suma de subtotal2
    print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    print("impresp",imp.id)
    sub2_pro=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        sub2_pro.append(valores.cantidad*valores.valor_unitario)
        producto_id.append(valores.id)
    

    # saveDetalleImportacion
    suma_subt2=sum(sub2_pro)
    print(producto_id)
    # print("factura id",extra_tienda)
    return  suma_subt2

def subtotal1(id_imp):
    ##Suma de subtotal1
    print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    print("impresp",imp.id)
    das_imp=Das.objects.get(importacion=imp)
    print("DAS",das_imp.id)
    sub1_merc=[]
    for valores in Detalle_das.objects.filter(das=das_imp):
        sub1_merc.append(valores.subtotal1)
    suma_subt1=sum(sub1_merc)
    # print("factura id",extra_tienda)
    return  suma_subt1

def validacion(subt1,subt2):
    #Si es igual me devuelve 1 sino me devuelve un cero
    if subt1==subt2:
        var=1
    else:
        var=0   
    return  var

def aranceles(id_imp):
    #Calculos de advalorem, fodinfa e iva
    print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    print("impresp",imp.id)
    das_imp=Das.objects.get(importacion=imp)
    print("DAS",das_imp.id)
    advalorem=[]
    fodinfa=[]
    iva=[]

    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        print(valores.subtotal2)
        for valor in Detalle_das.objects.filter(das=das_imp):
            if valores.mercancia==valor.mercancia:  
                advalorem.append(float(valores.subtotal2/(valor.subtotal1*valor.advalorem1)))
                fodinfa.append(float(valores.subtotal2/(valor.subtotal1*valor.fodinfa1)))
                iva.append(float(valores.subtotal2/(valor.subtotal1*valor.iva1)))
                print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.advalorem1 ," ") 
    print(advalorem)
    print(fodinfa)
    print(iva)

    return [advalorem,fodinfa,iva]


def sumaPeso(id_imp):
    print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    print("impresp",imp.id)
    pesos=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        pesos.append(valores.peso)
    suma_peso=sum(pesos)
    print(suma_peso)
    # print("factura id",extra_tienda)
    return  suma_peso


