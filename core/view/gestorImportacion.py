
from django.shortcuts import render, redirect

from ..controlador import buscarProductos
#from ..ecommerce import Woocommerce

from django.shortcuts import render, redirect
from django.utils.html import escape
from ..models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from django.http import HttpResponse
from woocommerce import API
from ..forms import UserRegisterForm, ProductRegister, FormImportacion, FormDas,FormFacturaProveedor,FormFacturaAfianzado,FormDetalleAfianzado


from django.contrib import messages
import json


def crearImportacion(request):
    print("estoy denr¡ntro de crear importAIOCN")
    if request.method == 'POST':
        print("estoy denr¡ntro de crear importAIOCN")

        list_sku = request.POST.get('skus')
        print(list_sku)
        productos=buscarProductos(list_sku)
        print(productos)
        print(productos)
    return render(request, 'core/crear_importacion.html', productos )


def startImport(request):
    
    if request.method=='POST':
        form=FormImportacion(request.POST)
        if form.is_valid():
            fecha=form['fecha'].value()
            form.save()
            proveedores=Proveedor.objects.select_related().all()
            cantidad=request.POST.get('cantidad')
            cant=[]
            for k in  range(int(cantidad)):
                cant.append(k)
            print(cantidad)
            fecha=Importacion.objects.last()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/proveedor.html',{"cantidad":cant,"cant":cantidad,"proveedores":proveedores,'fecha':fecha})
        else: 
            form=FormImportacion()
            messages.success(request, 'No se ha podido registrar! ')
            context={
                'form':form
            }
        return render(request,'core/importacion.html',context)
    else: 
        form=FormImportacion()
    
        context={
                'form':form
            }
    
    return render(request,'core/importacion.html',context)


# Create your views here.


def inicio(request):
    return render(request,'core/inicio.html')
def home(request):
   

    return render(request,'core/home.html')

def login(request):
    return render(request,'core/login.html')
 



def password(request):
    return render(request,'core/password.html')

def calcular(request):
    if "checkbox" in request.POST:
        product_id=request.POST.getlist('checkbox')
        precio=request.POST.getlist('pre')
        sub=request.POST.getlist('sub')
        cantidad=request.POST.getlist('cantidad')
        proveedor=request.POST.getlist('proveedor')
        mercancia=request.POST.getlist('mercancia')
        print(product_id)
        print(precio)
        print(sub)
        print(cantidad)
        print(proveedor)
        print(mercancia)
    return HttpResponse("<h1>"+str(product_id)+"</h>")

def register(request):
    if request.method=='POST':
        print('segundo formulaei')
        form=UserRegisterForm(request.POST)
        print(form)
        pas=form['password1'].value()
        username=form['password2'].help_text
        print("ddddddddddddddddddddddddd",username)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return redirect(request,'core/register.html')
        else: 
            form=UserRegisterForm()
            messages.success(request, 'No se ha podido registrar! La clave de contener numeros, letras mayusculas y minusculas, y debe contener mas de 8 carateres ')
            context={
                'form':form
            }
        return render(request,'core/register.html',context)
    else:
        
        form=UserRegisterForm()
    
        context={
                'form':form
            }
    print(context)
    return render(request,'core/register.html',context)

def saveProduct(request):
    if request.method=='POST':
        form=ProductRegister(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/product.html')
        else: 
            form=ProductRegister()
            messages.success(request, 'No se ha podido registrar! ')
            context={
                'form':form
            }
        return render(request,'core/product.html',context)
    else: 
        form=ProductRegister()
    
        context={
                'form':form
            }
    print(context)
    return render(request,'core/product.html',context)



def editar(request,id):
    datos = Importacion.objects.get(id=id)  
    context={
                'form':FormImportacion(instance=datos)
            }
    if request.method=='POST':
        form=FormImportacion(request.POST,instance=datos)
        if form.is_valid():
            fecha=form['fecha'].value()
            form.save()
            proveedores=Proveedor.objects.select_related().all()
            cantidad=request.POST.get('cantidad')
            cant=[]
            for k in  range(int(cantidad)):
                cant.append(k)
            print(cantidad)
            fecha=Importacion.objects.select_related().last()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/proveedor.html',{"cantidad":cant,"cant":cantidad,"proveedores":proveedores,'fecha':fecha})


    return render(request,'core/importacion.html',context)
# def actualizar(request,id):
#     datos = Importacion.objects.get(id=id) 
#     form=FormImportacion(request.POST,instance=datos) 
#     if form.is_valid():
#         form.save()
#         fecha=form['fecha'].value()
#         proveedores=Proveedor.objects.select_related().all()
#         cantidad=request.POST.get('cantidad')
#         cant=[]
#         for k in  range(int(cantidad)):
#             cant.append(k)
#         print(cantidad)
        
#         messages.success(request, 'Se ha registrado correctamente!')
#     return render(request,'core/proveedor.html',{"cantidad":cant,"cant":cantidad,"proveedores":proveedores,'fecha':datos})
    






