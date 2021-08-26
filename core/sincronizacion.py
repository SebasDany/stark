


from core.utilidades import updateActualizacionTienda, updateCost_Invent, updateIdWooProduct
from .models import Detalle_importacion

from django.conf import settings
from django.db import DatabaseError

import logging
from woocommerce import API
from core.woo_commerce import Woocommerce


class Sincronizacion:
    def __init__(self):
        self.wc = Woocommerce()
        self.logger = logging.getLogger(__name__)

    def extraerDatosBase(self,id):
        id_dI=[]
        cantidad_base=[]
        costoUnitario=[]
        #print("\tDatos de base de db_stark " )
        #print("\t Cantidad \t Costo_unitario \t SKU \t Nombre Producto" )
        
        for valores in Detalle_importacion.objects.filter(importacion=id).order_by('id'):
            #print(valores.id)
            id_dI.append(valores.id)
            cantidad_base.append(valores.cantidad)
            costoUnitario.append(valores.costo_unitario)
        #print("Base", cantidad_base,costoUnitario)
        
        
            #print("\t",valores.cantidad,'\t\t' ,valores.costo_unitario,"\t\t",valores.producto.sku,"\t\t",valores.producto.nombre)
        datos={
                "id_dI":id_dI,
                "cantidad_base":cantidad_base,
                "costoUnitario":costoUnitario,
                }
                    
        return datos

    def extraerDatosTienda(self, id):
        purchase_price=[]
        cantida_tienda=[]
        tipo_producto=[]
        

        no_encontrado=[]
        error1=''
        error=True
        #print("\tDatos de tienda de pruebas " )
        #print("\t Cantidad \t Costo_unitario \t SKU \t Nombre Producto" )
        for dt in  Detalle_importacion.objects.filter(importacion=id).order_by('id'):
            product =self.wc.get_producto_by_sku(dt.producto.sku)           
           
            if type(product) is dict:
                #print("estatid code ",product.get('data').get('status'))
                error1=True
            
            else:
                error1=False
                
            
                if(len(product)!=0):
                    error=False
                    if (len(product)!=0 and product[0].get('type')=='simple'):
                        
                        if  product[0].get('stock_quantity')==None:
                            purchase_price.append(product[0].get('purchase_price'))
                            cantida_tienda.append(0)
                            tipo_producto.append(0)
                        else:       
                            purchase_price.append(product[0].get('purchase_price'))
                            cantida_tienda.append(product[0].get('stock_quantity'))
                            tipo_producto.append(0)
                        updateIdWooProduct(dt.producto.id,product[0].get('id'),0)
                    
                    if(len(product)!=0 and product[0].get('type')=='variation' ):
                        padre=self.wc.get_producto_by_sku(dt.producto.sku.split("-")[0])
                     
                        if  product[0].get('stock_quantity')==None:
                            purchase_price.append(product[0].get('purchase_price'))
                            cantida_tienda.append(0)
                            tipo_producto.append(1)
                        else:
                            purchase_price.append(product[0].get('purchase_price'))
                            cantida_tienda.append(product[0].get('stock_quantity'))
                            tipo_producto.append(1)
                        updateIdWooProduct(dt.producto.id,padre[0].get('id'), product[0].get('id'))
                else:
                    #print("no se ha encontardo el producto con este sku",dt.producto.sku, " iteracion " )  
                    no_encontrado.append(dt.producto.sku)
                    purchase_price.append(0)
                    cantida_tienda.append(0)
                    tipo_producto.append(0) 
                    error=False 
            #print("\t", product[0].get('stock_quantity'),"\t\t",product[0].get('purchase_price'),"\t\t",product[0].get('sku'),"\t\t",product[0].get('name') )
       # print()
           
        datos={ "error":error,
                "error1":error1,
                "purchase_price":purchase_price,
                "cantida_tienda":cantida_tienda,
                "tipo_producto":tipo_producto,
                "no_encontrado":no_encontrado
                }
        
                    
        return datos

    def calcular(self,id):
        nuevo_cost=[]
        nueva_cantidad=[]
        datoBase=self.extraerDatosBase(id)
        datosTienda=self.extraerDatosTienda(id)
        error=False
        purchase=0
        if datosTienda["error"]==False:
            for i in range(len(datosTienda["tipo_producto"])):
                t1= datoBase["costoUnitario"][i]*datoBase["cantidad_base"][i]
                if datosTienda["purchase_price"][i]==None:
                    purchase=0
                else:
                    purchase=datosTienda["purchase_price"][i]
                if(datosTienda["cantida_tienda"][i]<0 ):
                    t2= purchase*0
                    nv=datoBase["costoUnitario"][i]
                    t_cant=datoBase["cantidad_base"][i]+datosTienda["cantida_tienda"][i]#eliminar
                    
                else:
                    t2= purchase*datosTienda["cantida_tienda"][i]

                    t_cant=datoBase["cantidad_base"][i]+datosTienda["cantida_tienda"][i]#sacar del else
                    #print("total cantidad",datoBase["cantidad_base"][i],datosTienda["cantida_tienda"][i])
                    t_cost=float(t1)+float(t2)
                    #print("calculo", datoBase["costoUnitario"][i],datoBase["cantidad_base"][i] )
                    #print("suma",datoBase["cantidad_base"][i], datosTienda["cantida_tienda"][i])
                    nueva_cantidad.append(t_cant)
                    nv=t_cost/t_cant#sacar hasta aca
                nuevo_cost.append(nv)
                updateCost_Invent(datoBase["id_dI"][i],nv, t_cant)
        else :
            error:True 
        datos={ "error":error,
                "id_dI":datoBase["id_dI"],
                "tipo_producto":datosTienda["tipo_producto"],
                "nueva_cantidad":nueva_cantidad,
                "nuevo_costo":nuevo_cost
                }

        return datos
                    

    def sincronizar(self,id):

        for valor in Detalle_importacion.objects.filter(importacion=id).order_by('id'):
            if valor.producto.variacion==True:

                data = {
                        "purchase_price": str(valor.nuevo_costo),
                        "stock_quantity": valor.total_inventario
                        
                        }
    
                resp=self.wc.set_producto_variacion(valor.producto.id_woocommerce,valor.producto.parent_id,data)
                if resp=='OK':
                    updateActualizacionTienda(valor.id,'SI')

            else:
                
                data = {
                        "purchase_price": str(valor.nuevo_costo),
                        "stock_quantity": valor.total_inventario
                            }
              
                resp=self.wc.set_producto_simple(valor.producto.id_woocommerce,data)
                if resp=='OK':
                    
                    updateActualizacionTienda(valor.id,'SI')

                datos={"error":False,
                "mensaje":"Productos actualizados correctamemte"}
        return datos

                


