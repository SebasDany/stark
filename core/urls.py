from core.view import gestorAfianzado
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
    path('calcular',gestorImportacion.calcular,name='calcular'),
    path('product',gestorImportacion.saveProduct,name='product'),
    path('importacion',gestorImportacion.startImport,name='importacion'),
    #path('facturaproveedor',gestorImportacion.facturaProveedor,name='facturaproveedor'),
    
    

    path('editar/<int:id>/',gestorImportacion.editar,name='editar'),
    #path('actualizar/<int:id>/',views.actualizar,name='actualizar'),

    path('facturaproveedor',gestorProveedor.facturaProveedor,name='facturaproveedor'),
    path('datosdas',gestorDas.datosDas,name='datosdas'),
    path('detalledas',gestorDas.detalleDas,name='detalledas'),
    path('datosafianzado',gestorAfianzado.datosAfianzado,name='datosafianzado'),
    path('detalleafianzado',gestorAfianzado.detalleAfianzado,name='detalleafianzado'),
    path('crearimportacion',gestorImportacion.crearImportacion,name='crearimportacion'),

        ]))),
    

]