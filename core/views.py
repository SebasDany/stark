from django.shortcuts import render, redirect
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from django.http import HttpResponse
from woocommerce import API
from .forms import UserRegisterForm, ProductRegister, FormImportacion, FormDas,FacturaProveedor
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto

from django.contrib import messages
import json


# Create your views here.
def conexionApiWoo():
    
    wcapi = API(
        url="http://18.217.125.242/", # Your store URL
        consumer_key="ck_683236fc573061c7e21af53d9c73a53a8f205229", # Your consumer key
        consumer_secret="cs_767e7406490a81353255b4937c055ca1036c5dbf", # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3" # WooCommerce WP REST API version
    )
    products = wcapi.get("products")
    productos=products.json()

    print(products.status_code)
    #print(productos[2])
    print('----------------------')
    
#     id=productos[0].get('id')
#     sku=productos[0].get('sku')
#     name=productos[0].get('name')
#     type=productos[0].get('type')
#     description=productos[0].get('description')
#     price=productos[0].get('price')
#     regular_price=productos[0].get('regular_price')
#     sale_price=productos[0].get('sale_price')
#     categories=productos[0].get('categories')#.name
#     image=productos[0].get('images')#.src
#     print("puchase_price: ",productos[0].get('purchase_price'))
#     print("id : ",id)
#     print("sku : ",sku)
#     print("name : ",name)
#     print("type : ",type)
#     print("description : ",description)
#     print("price : ",price)
#     print("regular peice : ",regular_price)
#     print("sale price : ",sale_price)
#     print("categories : ",categories)
#     print("images : ",image)


#     print(productos[0].get('id'))

# #1602

#     id=productos[0].get('id')
#     data = {
#         "regular_price": "88888"
#     }


#     #wcapi.put("products/"+str(id),data)
#     print(productos[0].get('id'))

    return productos
def inicio(request):
    return render(request,'core/inicio.html')
def home(request):
    product=conexionApiWoo()
    print("=================")
    #print(product)
    productos=Producto.objects.select_related().all()
    proveedores=Proveedor.objects.select_related().all()
    mercancias=Mercancia.objects.select_related().all()
    print(proveedores[0].nombre)
    print(mercancias[2].nombre)
    
    productos=Producto.objects.all()
    for producto in productos:
        print(producto.mercancia)

    return render(request,'core/home.html',{"productos":productos,"proveedores":proveedores,"mercancias":mercancias})

def login(request):
    return render(request,'core/login.html')

def facturaProveedor(request):
    if request.method=='POST':
        
        form=FacturaProveedor(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/das.html')
        else: 
            form=FacturaProveedor()
            messages.success(request, 'No se ha podido registrar! ')
            context={
                'form':form
            }
        return render(request,'core/proveedor.html',context)
    else: 
        form=FacturaProveedor()
    
        context={
                'form':form
            }
    return render(request,'core/proveedor.html',context)

def das(request):
    ncajas=request.POST.getlist('ncajas')
    print("valores del rpovedor", ncajas)
    
    #fp=Factura_proveedor('sds',)



    # impor=Factura_proveedor(fecha=data,descripcion=descripcion,tipo="Pu",origen="Azaya")
    # impor.save()
    # print("valores de fecha",data,descripcion)
    #fp.save()

  
    # proveedor=request.POST.getlist('proveedor')
    # mercancia=request.POST.getlist('mercancia')
    if request.method=='POST':
        form=FormDas(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/das.html')
        else: 
            form=FormDas()
            messages.success(request, 'No se ha podido registrar! ')
            context={
                'form':form
            }
        return render(request,'core/das.html',context)
    else: 
        form=FormDas()
    
        context={
                'form':form
            }
    #print(context)
    return render(request,'core/das.html',context)
    



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

def saveImport(request):
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

def imporAtras(request,id):
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
    
    


