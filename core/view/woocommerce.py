from core.models import Detalle_importacion
from woocommerce import API

wcapi = API(
         url="http://18.217.125.242/", # Your store URL
        consumer_key="ck_d27e19bf8855d4c1e8a0e7dc3d652fa8cdb27643", # Your consumer key
        consumer_secret="cs_8e1544fe175c35d1af7b9f30fe5a03f185be5497", # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3" # WooCommerce WP REST API version
        )
    
def conexionApiWoo():
    
   
    products = wcapi.get("products")
    productos=products.json()

    print(products.status_code)
    #print(productos[2])
    print('----------------------')
    qty=productos[0].get('qty')
    id=productos[0].get('id')
    sku=productos[0].get('sku')
    name=productos[0].get('name')
    type=productos[0].get('type')
    description=productos[0].get('description')
    price=productos[0].get('price')
    regular_price=productos[0].get('regular_price')
    sale_price=productos[0].get('sale_price')
    categories=productos[0].get('categories')#.name
    image=productos[0].get('images')#.src
    print("cantidad ", qty)
    print("puchase_price: ",productos[0].get('purchase_price'))
    print("id : ",id)
    print("sku : ",sku)
    print("name : ",name)
    print("type : ",type)
    print("description : ",description)
    print("price : ",price)
    print("regular peice : ",regular_price)
    print("sale price : ",sale_price)
    print("categories : ",categories)
    print("images : ",image)


    print(productos[0].get('id'))

#1602

    id=productos[0].get('id')
    data = {
        "regular_price": "88888"
    }


    #wcapi.put("products/"+str(id),data)
    print(productos[0].get('id'))

    return wcapi 

def calcular(id):
   
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
        print("······································",valores.producto.sku)
        id_producto_base.append(valores.producto.id)
        sku_base.append(valores.producto.sku)
        cantidad_base.append(valores.cantidad)
        costo_producto_un.append(valores.costo_unitario)
        
    #sku=['EP003-220k','EP003-22','AA001','hola','EP003','AA002']
    sku=sku_base
    for i in range(len(sku)):
        
        r =wcapi.get("products",params={'sku':sku[i]}).json()
       
        if(len(r)!=0):
        
            if (len(r)!=0 and r[0].get('type')=='simple'):
                               
                id_producto_tienda.append(r[0].get('id'))
                purchase_price.append(r[0].get('purchase_price'))
                cantida_tienda.append(r[0].get('stock_quantity'))
                tipo_producto.append(0)
            
            if(len(r)!=0 and r[0].get('type')=='variation'):

                id_producto_tienda.append(r[0].get('id'))
                purchase_price.append(r[0].get('purchase_price'))
                cantida_tienda.append(r[0].get('stock_quantity'))
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
        
    print(nuevo_costo)

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
    print(datos)
  
    return datos


def sincronizar(id):
    
    datos=calcular(id)
    for i in range(len(datos["nuevo_costo"])):

        if datos["tipo_producto"][i]==1:
            print("soy una variacion ")

            nuevo=wcapi.get("products",params={'sku':datos["sku_base"][i].split("-")[0]}).json()
            data = {
          "purchase_price": datos["nuevo_costo"][i]
         }
            print(data)
            print(str(nuevo[0].get('id')), str(datos["id_producto_tienda"][i]))

            #wcapi.put("products/"+str(nuevo[0].get('id'))+"/variations/"+str(datos["id_producto_tienda"][i])+"", data)#actualiza purchase price de mi tienda de pruebas
        else:
            print(" no soy una variacion ")
            data = {
             "purchase_price": datos["nuevo_costo"][i]
                }
            print(data, str(datos["id_producto_tienda"][i]))

            #wcapi.put("products/"+str(datos["id_producto_tienda"][i]), data)#actualiza purchase price de mi tienda de pruebas
    
