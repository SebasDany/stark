
from woocommerce import API

class Woocommerce:

    ## Credenciales de la tienda
    
    def __init__(self):
        # Create object to connect to woo api
        self.wcapi = API(
            url="http://3.17.224.172/", # Your store URL
            consumer_key="ck_08810b8606578f3a5f8649d075a365f4f5d26f70", # Your consumer key
            consumer_secret="cs_e8b018ebad63d03deac1d9e2e446ad741fbd1291", # Your consumer secret
            wp_api=True, # Enable the WP REST API integration
            version="wc/v3" # WooCommerce WP REST API version
        )
    
    ## obtiene los pedidos en json

    def get_pedidos(self, after):
        url = 'orders/?per_page=50&after={}&order=asc'.format(after)
        pedidos = self.wcapi.get(url).json()
        return pedidos

    ##  obtiene los pedidos en json

    def get_pedido(self, id_pedido):
        url = 'orders/' + str(id_pedido)
        pedido = self.wcapi.get(url).json()
        return pedido

    def get_producto_by_sku(self, sku):#busca el producto mediante el sku dentro de la tienda
        product = self.wcapi.get("products",params={'sku':sku}).json()

        
        return product
    def get_producto_variation_by_parent_id(self, parent_id):#busca el producto mediante el sku dentro de la tienda
        product = self.wcapi.get("products/"+str(parent_id)+"/variations").json()

        
        return product


    def set_producto_simple(self, id_producto, data):#actualiza el producto simple dentro de la tienda
        request = self.wcapi.put(f"products/{id_producto}", data)
        if request.status_code != 200:
            return request.text
        else:
            return request.reason

    def set_producto_variacion(self, parent_id, id_variacion, data):#actualiza el producto variacion en la teinda
        request = self.wcapi.put(f"products/{parent_id}/variations/{id_variacion}", data)
        if request.status_code != 200:
            return request.text
        else:
            return request.reason

    def create_producto(self,data):#crea el producto simple dentro de la tienda
        request= self.wcapi.post("products", data)
        if request.status_code != 200:
            return request.text
        else:
            return request.reason

    
## crear productos con variaciones

    def create_producto_variacion(self,parent_id,data):#crea el producto de tipo variacion
        request= self.wcapi.post(f"products/{parent_id}/variations", data)
        if request.status_code != 200:
            return request.text
        else:
            return request.reason




