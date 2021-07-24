from core.view import gestorAfianzado, gestorProducto
from django.urls import include, path
from .view import gestorImportacion, gestorProveedor,gestorDas
from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.contrib import admin
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('administrador/', include((
        [
            path('register',gestorImportacion.register,name='register'),
    path('password',gestorImportacion.password,name='password'),
    path('productosimportados/<int:id>/<int:idas>/<int:idfa>/',gestorProducto.productosImportados,name='productosimportados'),
    path('product',gestorImportacion.saveProduct,name='product'),
    path('startimport',gestorImportacion.startImport,name='startimport'),
    #path('facturaproveedor',gestorImportacion.facturaProveedor,name='facturaproveedor'),
    
    

    path('importacion/<int:id>/',gestorImportacion.importacion,name='importacion'),
    #path('actualizar/<int:id>/',views.actualizar,name='actualizar'),
    path('startFP/<int:id>/',gestorProveedor.startFactProve,name='startFP'),
    path('facturaproveedor',gestorProveedor.facturaProveedor,name='facturaproveedor'),
    path('startdas/<int:id>/',gestorDas.startDas,name='startdas'),
    path('datosdas/<int:id>/<int:idas>/',gestorDas.datosDas,name='datosdas'),
    path('detalledas/<int:id>/<int:idas>/',gestorDas.detalleDas,name='detalledas'),


    path('creardetalleafianzado/<int:id>/<int:idas>/<int:idfa>/',gestorAfianzado.crearDetalleAfianzado,name='creardetalleafianzado'),
    path('startafianzado/<int:id>/<int:idas>/',gestorAfianzado.startAfianzado,name='startafianzado'),
    path('datosafianzado/<int:id>/<int:idas>/<int:idfa>/',gestorAfianzado.datosAfianzado,name='datosafianzado'),
    path('detalleafianzado/<int:id>/<int:idas>/<int:idfa>/',gestorAfianzado.detalleAfianzado,name='detalleafianzado'),
    path('detalleimportacion/<int:id>/<int:idas>/<int:idfa>/',gestorImportacion.detalleImportacion,name='detalleimportacion'),
    path('buscarproducto/<int:id>/<int:idas>/<int:idfa>/',gestorProducto.buscarProductos,name='buscarproducto'),
    path('viewproduct/<int:id>/<int:idas>/<int:idfa>/',gestorProducto.viewProduct,name='viewproduct'),
    path('addproductimport/<int:id>/<int:idas>/<int:idfa>/',gestorProducto.addProductImport,name='addproductimport'),

        ]))),
    

]