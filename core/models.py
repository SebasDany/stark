from core.woo_commerce import Woocommerce
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import messages


# Create your models here.
class Mercancia(models.Model):
    nombre=models.CharField(max_length=80)
    subpartida=models.CharField(max_length=128)
    por_advalorem= models.DecimalField(max_digits=9, decimal_places=4, default=0)
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    mercancia=models.ForeignKey(Mercancia, on_delete=models.CASCADE, null=True,blank=True, default=None)
   
    id_woocommerce=models.IntegerField(default=0,blank=True)
    sku=models.CharField(max_length=16,unique=True)
    nombre=models.CharField(max_length=80)
    precio_compra=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    precio_neto = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    variacion = models.BooleanField(default=False)
    parent_id = models.IntegerField(default=0, blank=True)
    imagen = models.URLField(default='', blank=True)
    categorias = models.CharField(max_length=512, blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        s=len(self.sku.split("-"))
        if self.variacion == True and s==1:
            raise  ValidationError ("El sku de una variacion sigue esta estructura SKU-123")
        if self.variacion == False and s > 1:
            raise  ValidationError ("El sku de una de un producto simple sigue esta estructura SKU123")
        woo = Woocommerce()
        producto=woo.get_producto_by_sku(self.sku)
        if type(producto) is dict:
            if(producto.get('data').get('status')==401):
                
                raise  ValidationError ("No se ha podido conectar a la tienda error autenticacion")
        
        if len(producto)!=0:#verifica si esxite o no el producto dentro de la tienda
             raise  ValidationError ("El prodcuto "+ "SKU: " + str(producto[0].get('sku')) + ", \nNombre : " + str(producto[0].get('name'))+" YA EXISTE")
        if ( self.variacion == True and s!=1):
            padre=producto=woo.get_producto_by_sku(str(self.sku).split('-')[0])
            if(len(padre)==0):
                raise  ValidationError ("El producto  padre no existe debe crearse en la tienda de forma manual se debe traer el id del padre")



    def save(self, *args, **kwargs):
        woo = Woocommerce()        
        if(self.variacion==True):
            padre=producto=woo.get_producto_by_sku(str(self.sku).split('-')[0])
            data1 = {
                    "regular_price": str(self.precio_neto),
                    "purchase_price": 0,
                    "stock_quantity":0,
                    "atum_controlled": True,
                    "manage_stock":True,
                    "sku":str(self.sku),
                    "image": {
                        "id": 423
                    },
                    "attributes": [
                        {
                            "id": 9,
                            "option": "Black"
                        }
                    ]
                }
            woo.create_producto_variacion(str(padre[0].get('id')), data1)
            
            
        else:
            if(len(self.imagen)==0):
                src="http://3.17.224.172/wp-content/uploads/2021/08/cropped-logo_gsuite-1.png"
            else:
                src=str(self.imagen)
            data = {
                    "name": str(self.nombre),
                    "type": "simple",
                    "sku":str(self.sku),
                    "regular_price": str(self.precio_neto),
                    "purchase_price": 0,
                    "atum_controlled": True,
                    "description": " ",
                    "manage_stock":True,
                    "stock_quantity":0,
                    "short_description": "",
                    "categories": [
                    
                    ],
                    "images": [
                        {
                            "src": src
                        },   
                    ]
                }

            woo.create_producto(data)
        self.iva=float(self.precio_compra)*0.12
        self.precio_neto = float(self.iva)+float(self.precio_compra)
        super(Producto, self).save(*args, **kwargs) # Call the "real" save() method.
        
        
    def __str__(self):
        return self.nombre
    



class Afianzado(models.Model):
    ruc=models.CharField(max_length=128)
    nombre=models.CharField(max_length=255)
    direccion=models.CharField(max_length=255)
    def __str__(self):
        return self.nombre + "["+self.ruc+"]"


class Proveedor(models.Model):
    codigo=models.CharField(max_length=64, blank=True)
    nombre=models.CharField(max_length=64, blank=True)
    pais=models.CharField(max_length=64, blank=True)
    telefono=models.CharField(max_length=64, blank=True)
    def __str__(self):
        return self.nombre
        
class Importacion(models.Model):
    fecha=models.DateField(null = False)
    descripcion=models.CharField(max_length=64, blank=True)
    tipo=models.CharField(max_length=64, blank=True)
    origen=models.CharField(max_length=64, blank=True)
    estado=models.IntegerField(default=1)
    def __str__(self):
        
        return str(self.fecha)

class Factura_proveedor(models.Model):
    proveedor=models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True,blank=True, default=None)
    importacion=models.ForeignKey(Importacion, on_delete=models.CASCADE, null=True,blank=True, default=None)
    
    num_cajas=models.IntegerField(default=1)
    valor_factura=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    valor_envio=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    comision_envio=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    comision_tarjeta=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    isd=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    total_pago=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    extra=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    

class Proveedor_producto(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE, null=True,blank=True, default=None)
    proveedor=models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True,blank=True, default=None)
    sku=models.CharField(max_length=16)
    nombre=models.CharField(max_length=255)
    precio= models.DecimalField(max_digits=9, decimal_places=4, default=0)
    peso=models.DecimalField("Peso unitario (g)",max_digits=9, decimal_places=4, default=0)
    cantidad=models.IntegerField(default=0)
    def __str__(self):
        return self.nombre
    

class Das(models.Model):
    importacion=models.OneToOneField(Importacion, on_delete=models.CASCADE, null=True,blank=True, default=None)
    
   
    numero_entrega=models.CharField(max_length=128,null=True,blank=True)
    numero_atribuido= models.CharField(max_length=64)
    
    fecha_embarque=models.DateField(null = False )
    fecha_llegada=models.DateField(null = False)
    documento_transporte=models.CharField(max_length=64)
    tipo_carga=models.CharField(max_length=64,null=True,blank=True)
    pais_procedncia=models.CharField(max_length=255,null=True,blank=True)
    via_transporte=models.CharField(max_length=64,null=True,blank=True)
    puerto_enbarque=models.CharField(max_length=128,null=True,blank=True)
    ciudad_importador=models.CharField(max_length=128,null=True,blank=True)
    empresa_tranporte=models.CharField(max_length=128,null=True)
    
    identificacion_carga=models.CharField(max_length=128,null=True,blank=True)
    monto_flete=models.DecimalField(max_digits=9, decimal_places=2, default=0,null=True,blank=True)
    total_items=models.IntegerField(default=0,null=True,blank=True)
    peso_neto=models.DecimalField(max_digits=9, decimal_places=2, default=0,blank=True)
    total_bultos=models.IntegerField(default=0)
    unidades_comerciales=models.IntegerField(default=0)
    total_tributos=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    valor_seguros=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    cif=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    peso_bruto=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    unidades_fisicas=models.IntegerField(default=0)
    valor_fob=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    def __str__(self):
        return self.numero_atribuido

class Detalle_das(models.Model):
    mercancia=models.ForeignKey(Mercancia, on_delete=models.CASCADE, null=True,blank=True, default=None)
    das=models.ForeignKey(Das, on_delete=models.CASCADE, null=True,blank=True, default=None)
    advalorem1=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    fodinfa1=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    iva1=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    subtotal1=models.DecimalField(max_digits=9, decimal_places=4, default=0)



class Detalle_importacion(models.Model):
    SI='SI'
    NO='NO'
    estado_actualizaciOn = [
                        (SI, 'SI'),
                        (NO, 'NO') ]
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE, null=True,blank=True, default=None)
    das=models.ForeignKey(Das, on_delete=models.CASCADE, null=True,blank=True, default=None)#aumentado
    importacion=models.ForeignKey(Importacion, on_delete=models.CASCADE, null=True,blank=True, default=None)
    mercancia=models.ForeignKey(Mercancia, on_delete=models.CASCADE, null=True,blank=True, default=None)
    proveedor=models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True,blank=True, default=None)
   
    cantidad=models.IntegerField(default=0)
    novedades=models.CharField(max_length=255, blank=True)
    valor_unitario=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    subtotal2=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    peso=models.IntegerField(default=0)
    advalorem2=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    fodinfa2=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    iva2=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    ps=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    pr=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    prt=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    costo1=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    costo2=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    costo3=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    costo_unitario=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    inc_porcentual=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    inc_dolares=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    nuevo_costo=models.DecimalField(max_digits=9,decimal_places=4, default=0 )
    total_inventario=models.IntegerField(default=0 )
    actualizado= models.CharField(
        max_length=2,
        choices=estado_actualizaciOn,
        default=NO,
    )

class Factura_afianzado(models.Model):
    afianzado=models.ForeignKey(Afianzado, on_delete=models.CASCADE, null=True,blank=True, default=None)
    importacion=models.OneToOneField(Importacion, on_delete=models.CASCADE, null=True,blank=True, default=None)
    
    fecha=models.DateField()
    numero=models.CharField(max_length=64, blank=True)
    subtotal=models.DecimalField(max_digits=9, decimal_places=2)
    def __str__(self):
        return str(self.fecha)


class Detalle_afianzado(models.Model):
    factura_afianzado=models.ForeignKey(Factura_afianzado, on_delete=models.CASCADE, null=True,blank=True, default=None)
    descripcion=models.CharField(max_length=255, blank=True)
    al_peso=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    al_precio=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    
    iva=models.DecimalField(max_digits=9, decimal_places=4, default=0)
    total=models.DecimalField(max_digits=9, decimal_places=4, default=0)

class Historial(models.Model):
    importacion=models.OneToOneField(Importacion, on_delete=models.CASCADE, null=True,blank=True, default=None)
    
    #importacion=models.IntegerField(default=0)
    das=models.IntegerField(default=0)
    afianzado=models.IntegerField(default=0)
    estado=models.IntegerField(default=0)