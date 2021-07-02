from django.shortcuts import render
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from django.http import HttpResponse
from woocommerce import API
from .forms import UserRegisterForm
from django.contrib import messages
# Create your views here.
def conexionApiWoo():
    
    wcapi = API(
        url="http://18.217.125.242/", # Your store URL
        consumer_key="ck_683236fc573061c7e21af53d9c73a53a8f205229", # Your consumer key
        consumer_secret="cs_767e7406490a81353255b4937c055ca1036c5dbf", # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3" # WooCommerce WP REST API version
    )
    r = wcapi.get("products")
    dato=r.json()


    print(r.status_code)
    print(dato)
    print('----------------------')
    print(dato[0].get('id'))
    id=dato[0].get('id')
    data = {
        "regular_price": "88888"
    }


    #wcapi.put("products/"+str(id),data)
    print(dato[0].get('id'))

    return dato
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
            return render(request,'core/register.html')

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