
from requests.api import get
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto

import numpy as np  

def buscarProductos(skus):
    sku=skus.split(';')
    pr =[] 
    provedor_prod=[]
    result, indices=np.unique(sku,return_index=True) 
    print(result) 
    # print(result)  
    # print(indices ) 
    # print(sku[indices] )
    for i in  range(len(result)):
        p = Producto.objects.get(sku=result[i])
        pr_p=Proveedor_producto.objects.get(producto=p.id)
        print(pr_p)
        provedor_prod.append(pr_p)
        #pr.append(pr_p)
        pr.append(p)
    

    
    proveedores=Proveedor.objects.select_related().all()
    mercancias=Mercancia.objects.select_related().all()
    
        

    return {'error':False,
    "productos":pr,
    "pr_p":provedor_prod,
    "proveedores":proveedores,
    "mercancias":mercancias
            }

def saveDetalleImportacion(peso=[],precio=[],cantidad=[],id_prod=[],mercancia=[],proveedor=[]):
    dtdas=Detalle_das.objects.last()
    factProv=Factura_proveedor.objects.last()
    importacion=Importacion.objects.last()

    for i in range(len(id_prod)):
        dtImport=Detalle_importacion()
        dtImport.producto=Producto.objects.get(id=id_prod[i])
        dtImport.detalle_das=dtdas
        dtImport.factura_proveedor=factProv
        dtImport.importacion=importacion
        dtImport.mercancia=Mercancia.objects.get(id=mercancia[i])
        dtImport.proveedor=Proveedor.objects.get(id=proveedor[i])
        dtImport.valor_unitario=precio[i]
        dtImport.cantidad=cantidad[i]
        dtImport.peso=peso[i]
        dtImport.save()

    
    return {'error':False}    

def saveFacuturaProveedor(prove=[],fechaImport='',ncajas=[],v_envio=[],v_factura=[],comis_envio=[],comis_tarjeta=[],isd=[],t_pago=[],extra=[]):
    
    for i in range (len(prove)):
        fp = Factura_proveedor()
        try:
            #entero = int(posible_numero)

            fp.proveedor=Proveedor.objects.get(id = prove[i])
            fp.importacion=Importacion.objects.get(id=fechaImport)
            fp.num_cajas=ncajas[i]
            fp.valor_factura=v_factura[i]
            fp.valor_envio=v_envio[i]
            fp.comision_envio=comis_envio[i]
            fp.comision_tarjeta=comis_tarjeta[i]
            fp.isd=isd[i]
            fp.total_pago=t_pago[i]
            fp.extra=extra[i]
            fp.save()            
            print("Lo que escribiste es un entero")
            estado=False
        except ValueError:
            estado=True

    return {'error':estado}

def saveDas(idfechaImport,numero_atribuido,numero_entrega,
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
    
    #das.save() #Contiene una realcion de uno auno

    return {'error':False}

def saveDetalleDas(mercancia=[],advalorem=[],fodinfa=[],iva=[]):

    das=Das.objects.last()# obtiene el utlimo dato del la consulta
    
    for i in  range(len(mercancia)):
        dD=Detalle_das()
        
        dD.mercancia=Mercancia.objects.get(id = mercancia[i])
        dD.das=das
        dD.advalorem1=advalorem[i]
        dD.fodinfa1=fodinfa[i]
        dD.iva1=iva[i]
        dD.save()
        print(i)

    return {'error':False}

def saveAfianzado(afianzado,idfechaImport,fecha,numero,subtotal):
    af=Factura_afianzado()

    af.afianzado=Afianzado.objects.get(id=afianzado)
    af.importacion=Importacion.objects.get(id=idfechaImport)
    af.fecha=fecha
    af.numero=numero
    af.subtotal=subtotal
    #af.save() #Descomentar relacion de uno a uno entre eimprotaacion y factua afianzado
    afz=Factura_afianzado.objects.last()
    
    cant=[]
    for k in  range(4):
        cant.append(k)

   

    return {'error':False,
            'cantidad':cant, 
            'afz':afz
            }
def saveDetalleAfianzado(af=[],desc=[],ape=[],apr=[],iv=[], t=[]):

    faf=Factura_afianzado.objects.get(id=af[0])

    for i in  range(len(af)):
        dA=Detalle_afianzado()
        dA.factura_afianzado=faf
        dA.descripcion=desc[i]
        dA.al_peso=ape[i]
        dA.al_precio=apr[i]
        dA.iva=iv[i]
        dA.t=t[i]
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





