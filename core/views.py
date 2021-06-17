from django.shortcuts import render
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from django.http import HttpResponse

# Create your views here.

def home(request):
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

def register(request):
    return render(request,'core/register.html')

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