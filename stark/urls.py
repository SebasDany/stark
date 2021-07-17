"""stark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import viewss
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from core import views 


urlpatterns = [
    #path('',views.inicio,name='inicio'),
    path('',login_required(views.home),name='home'),
    # #path('login',views.login,name='login'),
    # path('register',views.register,name='register'),
    # path('password',views.password,name='password'),
    # path('calcular',views.calcular,name='calcular'),
    # path('product',views.saveProduct,name='product'),
    # path('importacion',views.saveImport,name='importacion'),
    # path('facturaproveedor',views.facturaProveedor,name='facturaproveedor'),
    
    

    # path('editar/<int:id>/',views.editar,name='editar'),
    # #path('actualizar/<int:id>/',views.actualizar,name='actualizar'),

    # path('das',views.das,name='das'),
    # path('detalledas',views.detalleDas,name='detalledas'),
    # path('facturaafianzado',views.facturaAfianzado,name='facturaafianzado'),
    # path('detalleafianzado',views.detalleAfianzado,name='detalleafianzado'),
    # path('detalleimportacion',views.detalleImportacion,name='detalleimportacion'),
    
    path('admin/', admin.site.urls),
    path('accounts/login/',LoginView.as_view(template_name='core/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='core/inicio.html'),name='logout'),
    path('', include('core.urls'), name='home'),
    
]
