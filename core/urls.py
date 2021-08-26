from core.view import gestorAfianzado, gestorProducto
from django.urls import include, path
from .view import gestorImportacion, gestorProveedor,gestorDas,importacion
from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.contrib import admin
from django.contrib.auth.decorators import login_required

urlpatterns = [

    
    path('administrador/', include((
        [
            path('register',login_required(importacion.register),name='register'),
    path('password',importacion.password,name='password'),
    
    path('product',login_required(importacion.saveProduct),name='product'),
    path('startimport',login_required(importacion.startImport),name='startimport'),
    

    path('importacion/<int:id>/',login_required(importacion.importacion),name='importacion'),
    #path('actualizar/<int:id>/',views.actualizar,name='actualizar'),
    path('startFP/<int:id>/',login_required(gestorProveedor.startFactProve),name='startFP'),
    #path('facturaproveedor',gestorProveedor.facturaProveedor,name='facturaproveedor'),
    path('startdas/<int:id>/',login_required(gestorDas.startDas),name='startdas'),
    path('datosdas/<int:id>/<int:idas>/',login_required(gestorDas.datosDas),name='datosdas'),
    path('detalledas/<int:id>/<int:idas>/',login_required(gestorDas.detalleDas),name='detalledas'),


    path('creardetalleafianzado/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorAfianzado.crearDetalleAfianzado),name='creardetalleafianzado'),
    path('startafianzado/<int:id>/<int:idas>/',login_required(gestorAfianzado.startAfianzado),name='startafianzado'),
    path('datosafianzado/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorAfianzado.datosAfianzado),name='datosafianzado'),
    path('detalleafianzado/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorAfianzado.detalleAfianzado),name='detalleafianzado'),
    
   
    path('buscarproducto/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.buscarProductos),name='buscarproducto'),
    path('viewproduct/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.viewProduct),name='viewproduct'),
    path('addproductimport/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.addProductImport),name='addproductimport'),
    path('viewresults/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.viewResults),name='viewresults'),
    path('detalleimportacion/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.detalleImportacion),name='detalleimportacion'),
    path('productosimportados/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.productosImportados),name='productosimportados'),
    path('previewsyncronizar/<int:id>/<int:idas>/<int:idfa>/',login_required(gestorImportacion.previewSyncronizar),name='previewsyncronizar'),
    path('updatetienda/<int:id>/',login_required(gestorImportacion.updateTienda),name='updatetienda'),
    path('listresults/<int:id>/',login_required(gestorImportacion.listresults),name='listresults'),
    
    


        ]))),
    

]