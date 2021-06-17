from django.contrib import admin
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto


# Register your models here.
admin.site.register(Mercancia)
admin.site.register(Producto)
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