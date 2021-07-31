
from woocommerce import API

class Woocommerce:
    def __init__(self):
        # Create object to connect to woo api
        self.wcapi = API(
            url="http://18.217.125.242/", # Your store URL
            consumer_key="ck_d27e19bf8855d4c1e8a0e7dc3d652fa8cdb27643", # Your consumer key
            consumer_secret="cs_8e1544fe175c35d1af7b9f30fe5a03f185be5497", # Your consumer secret
            wp_api=True, # Enable the WP REST API integration
            version="wc/v3" # WooCommerce WP REST API version
        )
    
    
    def get_pedidos(self, after):
        url = 'orders/?per_page=50&after={}&order=asc'.format(after)
        pedidos = self.wcapi.get(url).json()
        return pedidos

    def get_pedido(self, id_pedido):
        url = 'orders/' + str(id_pedido)
        pedido = self.wcapi.get(url).json()
        return pedido

    def get_producto_by_sku(self, sku):
        product = self.wcapi.get("products",params={'sku':sku}).json()

        
        return product

    def set_producto_simple(self, id_producto, data):
        request = self.wcapi.put(f"products/{id_producto}", data)
        if request.status_code != 200:
            return request.text
        else:
            return request.reason

    def set_producto_variacion(self, parent_id, id_variacion, data):
        request = self.wcapi.put(f"products/{parent_id}/variations/{id_variacion}", data)
        if request.status_code != 200:
            return request.text
        else:
            return request.reason

    def create_producto_simple(self,data):
        request= self.wcapi.post("products", data).json()
        if request.status_code != 200:
            return request.text
        else:
            return request.reason

    def create_producto_variacion(self,data):
        request= self.wcapi.post("products", data).json()
        if request.status_code != 200:
            return request.text
        else:
            return request.reason



