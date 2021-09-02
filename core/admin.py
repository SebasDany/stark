from django.contrib import admin
from django.db import models
from .models import Afianzadoadmin, Dasadmin, Detalle_afianzadoadmin, Detalle_dasadmin, Detalle_importacionadmin, Factura_afianzadoadmin, Factura_proveedoradmin, Historial, Importacionadmin, Mercancia, MercanciaAdmin,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto, Proveedor_productoadmin, Proveedoradmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ProductoResource(resources.ModelResource):
    class Meta: 
        model= Producto
       
class ProductoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields=['sku']
    list_display=('id', 'mercancia', 'id_woocommerce', 'sku', 'nombre', 'precio_compra', 'precio_neto', 'iva', 'variacion', 'parent_id', 'imagen', 'categorias', 'observaciones')
    resource_class= ProductoResource







# Register your models here.
admin.site.register(Mercancia,MercanciaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Afianzado,Afianzadoadmin)
admin.site.register(Proveedor,Proveedoradmin)
admin.site.register(Importacion,Importacionadmin)
admin.site.register(Factura_proveedor,Factura_proveedoradmin)
admin.site.register(Proveedor_producto,Proveedor_productoadmin)
admin.site.register(Das,Dasadmin)
admin.site.register(Detalle_das,Detalle_dasadmin)
admin.site.register(Detalle_importacion,Detalle_importacionadmin)
admin.site.register(Factura_afianzado,Factura_afianzadoadmin)
admin.site.register(Detalle_afianzado,Detalle_afianzadoadmin)
admin.site.register(Historial)

