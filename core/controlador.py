
from .models import Historial, Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto

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
        #print(valores.id)
        precios.append(valores.al_precio)
        peso.append(valores.al_peso)
        iva.append(valores.iva)
    #print(precios, )
    sum_precios=sum(precios)
    sum_peso=sum(peso)
    sum_iva=sum(iva)
    # print("factura afianzado",sum(precios))
    # print("factura afianzado",sum(peso))
    # print("factura afianzado",sum(iva))
    datos={"sum_precios": sum_precios,
        "sum_peso": sum_peso,
        "sum_iva": sum_iva
        }
    return  datos

def subtotal2(id_imp):
    ##Suma de subtotal2
    # print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    # print("impresp",imp.id)
    sub2_pro=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        sub2_pro.append(valores.cantidad*valores.valor_unitario)
        producto_id.append(valores.id)
    
    # saveDetalleImportacion
    #print("suma subt2", sub2_pro)
    suma_subt2=sum(sub2_pro)
    #print("suma subt2", suma_subt2)
    datos={"producto_id": producto_id,
    "Subtotales2": sub2_pro,
    "SumaSub2": suma_subt2
    }
    # print("factura id",extra_tienda)
    return datos

def subtotal1(id_imp):
    print(" Actualizando el subtotal 1")
    ##Suma de subtotal1
    # print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    # print("impresp",imp.id)
    das_imp=Das.objects.get(importacion=imp)
    # print("DAS",das_imp.id)
    sub1_merc_t=[]
    sub1_merc=[]
    id_dd=[]
    ad_das=0
    fod_das=0
    iva_das=0
    for valores in Detalle_das.objects.filter(das=das_imp):
        acum=0 
        ad_das+=valores.advalorem1
        fod_das+=valores.fodinfa1
        iva_das+=valores.iva1
        for valor in Detalle_importacion.objects.filter(importacion=id_imp):
            if valores.mercancia==valor.mercancia:  
                #sub1_merc.append(valores.subtotal1)
                acum+=valor.subtotal2
        #suma_subt1=sum(sub1_merc)
        
        sub1_merc_t.append(acum)
        suma_sub1=sum(sub1_merc_t)
        id_dd.append(valores.id)
    print("suma",ad_das)
    datos={ "sub1_merc_t":sub1_merc_t,
                "id_dd":id_dd,
                "suma_sub1": suma_sub1,
                "ad_das": ad_das,
                "fod_das": fod_das,
                "iva_das": iva_das
        }
    # print("factura id",extra_tienda)
    return  datos

def validacion(subt1,subt2):
    #Si es igual me devuelve 1 sino me devuelve un cero
    if subt1==subt2:
        var=1
    else:
        var=0   
    return  var

def aranceles(id_imp):
    #Calculos de advalorem, fodinfa e iva
    # print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    # print("impresp",imp.id)
    das_imp=Das.objects.get(importacion=imp)
    # print("DAS",das_imp.id)
    advalorem=[]
    fodinfa=[]
    iva=[]

    producto_id=[]
    for valor in Detalle_das.objects.filter(das=das_imp):
        cont=0
        var=Detalle_importacion.objects.filter(mercancia=valor.mercancia)
        tam=len(var)
        #print(tam, valor.mercancia)
        for valores in Detalle_importacion.objects.filter(importacion=imp.id):
            
            cont=cont+1
            #print(valores.mercancia," ", valor.mercancia," " )
            #print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.advalorem1 ," ")
            #print (" contador",cont )
            if valores.mercancia==valor.mercancia:
                
                producto_id.append(valores.id)
                if valor.advalorem1==0:
                    advalorem.append(0)
                    #print ("advalorem0")
                if valor.fodinfa1==0:
                    fodinfa.append(0)
                    #print ("fodinfa 0")
                if valor.iva1==0:                 
                    iva.append(0)
                    #print ("iva 0")
                if tam==1: 
                    advalorem.append(valor.advalorem1)
                    fodinfa.append(valor.fodinfa1)
                    iva.append(valor.iva1)
                    #print ("tamaño 1")
                else:
                    advalorem.append((valores.subtotal2/valor.subtotal1)*valor.advalorem1)
                    fodinfa.append((valores.subtotal2/valor.subtotal1)*valor.fodinfa1)
                    iva.append((valores.subtotal2/valor.subtotal1)*valor.iva1)
        
                    #print("productos", cont, "mercancia", valor.mercancia )
        
                    #print(valores.producto," ", valores.subtotal2," ",valor.subtotal1," ", valor.fodinfa1 ," ") 
   # print("*********",len(fodinfa))

    suma_ad=sum(advalorem)
    suma_fod=sum(fodinfa)
    suma_iva=sum(iva)
    #print("*********",suma_ad)
    datos={"producto_id": producto_id,
        "advalorem": advalorem,
        "fodinfa": fodinfa,
        "iva": iva,
        "suma_ad":suma_ad,
        "suma_fod":suma_fod,
        "suma_iva":suma_iva,
        }

    return datos


def porcentuales(id_imp):
    # print("importacion",id_imp)
    imp = Importacion.objects.get(id=id_imp)
    # print("impresp",imp.id)
    pesos=[]
    ps=[]
    pr=[]
    prT=[]
    producto_id=[]
    for valor in Detalle_importacion.objects.filter(importacion=imp.id):
        pesos.append(valor.peso)
      
    suma_peso=sum(pesos)
    
    suma_subtotal2=subtotal2(id_imp)
    for valor in Factura_proveedor.objects.filter(importacion=imp.id):
        #print(suma_peso,"suma peso", valores.peso )
        
        
        for valores in Detalle_importacion.objects.filter(importacion=imp.id):
            ps.append(valores.peso/suma_peso)
            pr.append(valores.subtotal2/suma_subtotal2["SumaSub2"])
           
            if(valores.proveedor==valor.proveedor):
                #print("**************",valor.proveedor, " ",valor.valor_factura," ", valores.proveedor, " ",valores.subtotal2)
                prT.append(valores.subtotal2/valor.valor_factura)
                producto_id.append(valores.id)
    #print("PRT",prT)
    # print("**************",suma_subtotal2["SumaSub2"], " ", valores.subtotal2)
    datos={"producto_id": producto_id,
        "ps": ps,
        "pr": pr,
        "prT": prT
        }
    return  datos

def costos(id_imp):
    imp = Importacion.objects.get(id=id_imp)
    tabla_afianz=tablaAfianzado(id_imp)
    costo1=[]
    costo2=[]
    costo3=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        producto_id.append(valores.id)
        costo1.append((tabla_afianz["sum_precios"]+tabla_afianz["sum_iva"])*valores.pr)
        costo2.append(tabla_afianz["sum_peso"]*valores.ps)
        for valor in Factura_proveedor.objects.filter(importacion=imp.id):
            if(valores.proveedor==valor.proveedor):
                costo3.append(valor.extra*valores.prt)
                #print("**************",valor.proveedor, " ",valor.extra," ", valores.proveedor, " ",valores.prt)
        #print(valores.ps," ", tabla_afianz["sum_peso"] )
        #print(valores.pr," ", tabla_afianz["sum_precios"], " ", tabla_afianz["sum_iva"] )
    datos={"producto_id": producto_id,
        "costo1": costo1,
        "costo2": costo2,
        "costo3": costo3
        }
    return  datos


def costo_unitario(id_imp):
    imp = Importacion.objects.get(id=id_imp)
    costo1_unitario=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        producto_id.append(valores.id)
        costo1_unitario.append(valores.valor_unitario+((valores.advalorem2+valores.fodinfa2+valores.iva2+valores.costo1+valores.costo2+valores.costo3)/valores.cantidad))
        print(valores.producto," ",valores.valor_unitario, " ",valores.advalorem2," ",valores.fodinfa2," ",valores.iva2," ",valores.costo1," ",valores.costo2," ",valores.costo3," ",valores.cantidad)
    
    datos={"producto_id": producto_id,
        "costo1_unitario": costo1_unitario
        }
    return  datos


def incrementos(id_imp):
    imp = Importacion.objects.get(id=id_imp)
    inc_porcentual=[]
    inc_dolares=[]
    producto_id=[]
    for valores in Detalle_importacion.objects.filter(importacion=imp.id):
        producto_id.append(valores.id)
        inc_porcentual.append((valores.costo_unitario-valores.valor_unitario)/valores.valor_unitario)
        inc_dolares.append(valores.costo_unitario-valores.valor_unitario)
    #print(inc_porcentual,inc_dolares)
    datos={"producto_id": producto_id,
        "inc_porcentual": inc_porcentual,
        "inc_dolares": inc_dolares
        }
    return  datos

def updateEstado(id, estado):
    Importacion.objects.filter(id=id).update(estado=estado)
    return 1
def crearH(id,idas,idaf,estado):
    h=Historial()
    #h.impor=Importacion.objects.get(id=id)
    h.importacion=Importacion.objects.get(id=id)
    h.das=idas
    h.afianzado=idaf
    h.estado=estado
    h.save()
def updateH(id,idas,idaf,estado):
    h=Historial.objects.get(importacion=id)

    Historial.objects.filter(id=h.id).update(das=idas,afianzado=idaf,estado=estado)

