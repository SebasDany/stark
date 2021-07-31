


from .models import Detalle_importacion

from django.conf import settings
from django.db import DatabaseError

import logging
from woocommerce import API
from core.woo_commerce import Woocommerce





class Productos2Woocommerce:
    def __init__(self):
        self.wc = Woocommerce()
        self.logger = logging.getLogger(__name__)

    def procesar_producto_dt_i(self,id):
        id_producto_base=[]
        sku_base=[]
        cantidad_base=[]
        costo_producto_un=[]
        id_producto_tienda=[]
        purchase_price=[]
        cantida_tienda=[]
        tipo_producto=[]
        nuevo_costo=[]
      
        for valores in Detalle_importacion.objects.filter(importacion=id):
            id_producto_base.append(valores.producto.id)
            sku_base.append(valores.producto.sku)
            cantidad_base.append(valores.cantidad)
            costo_producto_un.append(valores.costo_unitario)
        
        sku=sku_base
        
        for i in range(len(sku)):
            producto =self.wc.get_producto_by_sku(sku[i])
            #get("products",params={'sku':sku[i]}).json()
            #print(wcapi.get("products",params={'sku':sku[i]}).json())
            print(producto)
            if(len(producto)!=0):
                if (len(producto)!=0 and producto[0].get('type')=='simple'):           
                    id_producto_tienda.append(producto[0].get('id'))
                    purchase_price.append(producto[0].get('purchase_price'))
                    cantida_tienda.append(producto[0].get('stock_quantity'))
                    tipo_producto.append(0)
                
                if(len(producto)!=0 and producto[0].get('type')=='variation'):
                    id_producto_tienda.append(producto[0].get('id'))
                    purchase_price.append(producto[0].get('purchase_price'))
                    cantida_tienda.append(producto[0].get('stock_quantity'))
                    tipo_producto.append(1)
            else:
                print("no se ha encontardo el producto con este sku",sku[i], " iteracion ",i )   

        for i in range(len(tipo_producto)):
            t1= costo_producto_un[i]*cantidad_base[i]
            t2= purchase_price[i]*cantida_tienda[i]
            t_cant=cantidad_base[i]+cantida_tienda[i]
            t_cost=float(t1)+float(t2)

            nv=t_cost/t_cant
            nuevo_costo.append(nv)

        datos={
                "id_producto_base":id_producto_base,
                "sku_base":sku_base,
                "cantidad_base":cantidad_base,
                "costo_producto_un":costo_producto_un,
                "id_producto_tienda":id_producto_tienda,
                "purchase_price":purchase_price,
                "cantida_tienda":cantida_tienda,
                "tipo_producto":tipo_producto,
                "nuevo_costo":nuevo_costo
                }
                    
        return datos
    
    def sincronizar(self,id):
    
        datos=self.procesar_producto_dt_i(id)
        for i in range(len(datos["nuevo_costo"])):
            if datos["tipo_producto"][i]==1:
                print("soy una variacion ")
                nuevo=self.wc.get_producto_by_sku(datos["sku_base"][i].split("-")[0])
                #wcapi.get("products",params={'sku':datos["sku_base"][i].split("-")[0]}).json()
                data = {
            "purchase_price": datos["nuevo_costo"][i]
            }
                print(data)
                print(str(nuevo[0].get('id')), str(datos["id_producto_tienda"][i]))
                self.wc.set_producto_variacion(str(nuevo[0].get('id')),str(datos["id_producto_tienda"][i]),data)

                #wcapi.put("products/"+str(nuevo[0].get('id'))+"/variations/"+str(datos["id_producto_tienda"][i])+"", data)#actualiza purchase price de mi tienda de pruebas
            else:
                print(" no soy una variacion ")
                data = {
                "purchase_price": datos["nuevo_costo"][i]
                    }
                print(data, str(datos["id_producto_tienda"][i]))
                self.wc.set_producto_simple(str(datos["id_producto_tienda"][i]),data)

                #wcapi.put("products/"+str(datos["id_producto_tienda"][i]), data)#actualiza purchase price de mi tienda de pruebas
        return {"error":False,
                "mensaje":"Productos actualizados correctamemte"}


    # def procesar(self):
    #     self.logger.info("** INICIO DE PROCESAMIENTO TOTAL **")
    #     # obtener productos
    #     productos = Producto.objects.all().order_by('sku')
    #     self.procesar_productos(productos)

    # def procesar_sku(self, sku):
    #     self.logger.info(f"** INICIO DE PROCESAMIENTO PARCIAL {sku} **")
    #     # obtener productos
    #     productos = Producto.objects.filter(sku__contains=sku).order_by('sku')
    #     self.procesar_productos(productos)

    # def procesar_imagenes(self):
    #     self.logger.info(f"** INICIO DE PROCESAMIENTO DE IMAGENES **")
    #     # obtener productos
    #     productos = Producto.objects.all().order_by('sku')
    #     total_productos = len(productos)
    #     self.logger.info(f"Total de productos a procesar: {total_productos}")
    #     # atender a cada producto
    #     i = 1
    #     for producto in productos:
    #         self.logger.info(f"Procesando producto {i}/{total_productos} {producto}")
    #         print(f"Procesando producto {i}/{total_productos} {producto}")
    #         producto_wc = self.wc.get_producto_by_sku(producto.sku)
    #         if len(producto_wc) == 0:
    #             self.logger.error(f'El producto {producto} NO existe en woocommerce')
    #             print(f'[ERROR] El producto {producto} NO existe en woocommerce')
    #         else:
    #             self.obtener_datos_woo(producto, producto_wc[0])
    #         i += 1

    # def procesar_productos(self, productos):
    #     total_productos = len(productos)
    #     self.logger.info(f"Total de productos a procesar: {total_productos}")
    #     # atender a cada producto
    #     i = 1
    #     for p in productos:
    #         self.logger.info(f"Procesando producto {i}/{total_productos} {p}")
    #         print(f"Procesando producto {i}/{total_productos} {p}")
    #         kardex = p.kardex_set.all()
    #         existencias = self.obtener_existencias(kardex)
    #         # self.establecer_precios(p)
    #         self.actualizar_woocommerce(p, existencias)
    #         i += 1

    # def establecer_precios(self, producto):
    #     """
    #     Funcion temporar para establecer los precios neto y sin iva a partir
    #     del precio de venta. Solo se utilizó una vez.
    #     """
    #     # establecer precio neto
    #     neto = float(producto.precio_venta) / 1.12
    #     iva = float(producto.precio_venta) - neto
    #     producto.precio_neto = neto
    #     producto.iva = iva
    #     self.logger.info(
    #         f"Actualizando precios {producto}: neto = {neto}, iva = {iva}, venta = {producto.precio_venta}")
    #     producto.save()

    # def obtener_existencias(self, kardex: Kardex):
    #     existencias = 0
    #     for k in kardex:
    #         existencias += k.existencias
    #     if existencias < 0:
    #         self.logger.warning(f"Existencias negativas {existencias} para {k.producto}")
    #     return existencias

    # def actualizar_woocommerce(self, producto, existencias):
    #     if producto.precio_venta <= 0:
    #         print(f'[WARNING] Producto {producto} con precio de venta {producto.precio_venta}')
    #         self.logger.warning(f'[WARNING] Producto {producto} con precio de venta {producto.precio_venta}')
    #     producto_wc = self.wc.get_producto_by_sku(producto.sku)
    #     if len(producto_wc) == 0:
    #         self.logger.error(f'El producto {producto} NO existe en woocommerce')
    #         print(f'[ERROR] El producto {producto} NO existe en woocommerce')
    #         return False
    #     # obtiene desde el Woocommerce la imagen, categorías y si se trata de un producto de variación.
    #     self.obtener_datos_woo(producto, producto_wc[0])
    #     if producto.variacion:
    #         data = {
    #             'price': str(producto.precio_neto),
    #             'regular_price': str(producto.precio_neto),
    #             'stock_quantity': str(existencias),
    #             'purchase_price': str(producto.precio_compra),
    #             # '_variation_description': producto.descripcion_corta
    #         }
    #         respuesta = self.wc.set_producto_variacion(producto.parent_id, producto.id_woo, data)
    #     else:
    #         data = {
    #             'name': producto.nombre,
    #             'price': str(producto.precio_neto),
    #             'regular_price': str(producto.precio_neto),
    #             'stock_quantity': str(existencias),
    #             # 'short_description': producto.descripcion_corta,
    #             # 'description': producto.descripcion,
    #             'purchase_price': str(producto.precio_compra)
    #         }
    #         respuesta = self.wc.set_producto_simple(producto.id_woo, data)
    #     if respuesta == 'OK':
    #         self.generar_sql_atum(producto.id_woo, producto.precio_compra)
    #         self.logger.debug(f'Procesando en woocommerce: {producto.sku}, {data}. Respuesta = {respuesta}')
    #     else:
    #         self.logger.error(f'No se pudo actualizar en woocommerce el producto {producto}: {respuesta}')
    #     return True

    # def obtener_imagen(self, registro_wc):
    #     if len(registro_wc['images']) > 0:
    #         return registro_wc['images'][0]['src']
    #     return ''

    # def obtener_datos_woo(self, producto, registro_wc):
    #     producto.id_woo = registro_wc['id']
    #     producto.parent_id = registro_wc['parent_id']
    #     producto.imagen = self.obtener_imagen(registro_wc)
    #     # verifica si el producto es simple o variacion
    #     if producto.parent_id > 0:
    #         producto.variacion = True
    #     # obtiene las categorias
    #     categorias = ''
    #     if len(registro_wc['categories']) > 0:
    #         for c in registro_wc['categories']:
    #             categorias += c['name'] + ','
    #     producto.categorias = categorias[:-1]
    #     # guarda los datos
    #     try:
    #         producto.save()
    #         self.logger.debug(f'Producto {producto.sku} actualizado desde Woocommerce')
    #     except DatabaseError as e:
    #         self.logger.error(f'No se puede guardar el producto {producto}: {e}')
    #         return False
    #     return True

    # def generar_sql_atum(self, id_producto, precio_compra):
    #     sql = "update wordpress.wp_atum_product_data set purchase_price = " + str(
    #         precio_compra) + " where product_id = " + str(
    #         id_producto) + ";"
    #     self.logger.debug(f'SQL: {sql}')
