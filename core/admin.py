from django.contrib import admin
from .models import Historial, Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CategoriaResource(resources.ModelResource):
    class Meta: 
        model= Producto
class CategoriaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields=['sku']
    list_display=('id', 'mercancia', 'id_woocommerce', 'sku', 'nombre', 'precio_compra', 'precio_neto', 'iva', 'variacion', 'parent_id', 'imagen', 'categorias', 'observaciones')
    resource_class= CategoriaResource

# Register your models here.
admin.site.register(Mercancia)
admin.site.register(Producto, CategoriaAdmin)
admin.site.register(Afianzado)
admin.site.register(Proveedor)
admin.site.register(Importacion)
admin.site.register(Factura_proveedor)
admin.site.register(Proveedor_producto)
admin.site.register(Das)
admin.site.register(Detalle_das)
admin.site.register(Detalle_importacion)
admin.site.register(Factura_afianzado)
admin.site.register(Detalle_afianzado)
admin.site.register(Historial)

