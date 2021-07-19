from django.shortcuts import render, redirect
from django.utils.html import escape
from .models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from django.http import HttpResponse
from woocommerce import API
from .forms import UserRegisterForm, ProductRegister, FormImportacion, FormDas,FormFacturaProveedor,FormFacturaAfianzado,FormDetalleAfianzado


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
   

    return render(request,'core/home.html')

def login(request):
    return render(request,'core/login.html')

def facturaProveedor(request):
    if request.method=='POST':
        
        form=FormFacturaProveedor(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/das.html')
        else: 
            form=FormFacturaProveedor()
            messages.success(request, 'No se ha podido registrar! ')
            context={
                'form':form
            }
        return render(request,'core/proveedor.html',context)
    else: 
        form=FormFacturaProveedor()
    
        context={
                'form':form
            }
    return render(request,'core/proveedor.html',context)

def das(request):
    fecha=request.POST.get('fecha')
    fechaImport=request.POST.get('idfechaImport')
    #fc=Importacion.objects.get(id = 365)
    
    prove= request.POST.getlist('proveedor')
    
    print("valor de proveedor",prove)
    ncajas=request.POST.getlist('ncajas')
    v_envio=request.POST.getlist('v_envio')
    v_factura=request.POST.getlist('v_factura')
    comis_envio=request.POST.getlist('comis_envio')
    comis_tarjeta=request.POST.getlist('comis_tarjeta')
    isd=request.POST.getlist('isd')
    t_pago=request.POST.getlist('t_pago')
    extra=request.POST.getlist('extra')

    
    print("valores del 1", fechaImport)
    print("valores del proveedor",prove)
    print("valores del ncajas",ncajas)
    print("valores del v_envio ",v_envio)
    print("valores delv_factura ",v_factura)
    print("valores del comis_envio ",comis_envio)
    print("valores del comis_tarjeta ",comis_tarjeta)
    print("valores del isd",isd)
    print("valores del t:pago",t_pago)
    print("valores del extra",extra)
    fp = Factura_proveedor()
    fp.proveedor=Proveedor.objects.get(id = prove[0])
    fp.importacion=Importacion.objects.get(id=fechaImport)
    fp.num_cajas=1
    fp.valor_factura=v_factura[0]
    fp.valor_envio=v_envio[0]
    fp.comision_envio=v_envio[0]
    fp.comision_tarjeta=comis_tarjeta[0]
    fp.isd=isd[0]
    fp.total_pago=t_pago[0]
    fp.extra=extra[0]

    # pr=Factura_proveedor(proveedor=pr,importacion=fc,num_cajas=ncajas[0],valor_factura=v_factura[0]
    # ,valor_envio=v_envio[0],comision_envio=comis_envio[0],comision_tarjeta=comis_tarjeta[0],isd=isd[0],total_pago=t_pago[0],extra=extra[0])
    # form=FormFacturaProveedor(pr)
    
    fp.save()
    print("datos ingresados corrctamente")
    #fp=Factura_proveedor('sds',)



    # impor=Factura_proveedor(fecha=data,descripcion=descripcion,tipo="Pu",origen="Azaya")
    # impor.save()
    # print("valores de fecha",data,descripcion)
    #fp.save()

  
    # proveedor=request.POST.getlist('proveedor')
    # mercancia=request.POST.getlist('mercancia')
    # cant=[]
    # for k in  range(int(cantidad)):
    #     cant.append(k)
    #     print(cantidad)
    fecha=Importacion.objects.last()
    
    #print(context)
    return render(request,'core/das.html',{'fecha':fecha})
    



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
    


def detalleDas(request):
    
    das = Das()
    das.importacion=Importacion.objects.get(id=request.POST.get('idfechaImport'))
    das.numero_atribuido=request.POST.get('numero_atribuido')
    das.numero_entrega=request.POST.get('numero_entrega')
    das.fecha_embarque=request.POST.get('fecha_embarque')
    das.fecha_llegada=request.POST.get('fecha_llegada')
    das.documento_transporte=request.POST.get('documento_transporte')
    das.tipo_carga=request.POST.get('tipo_carga')
    das.pais_procedncia=request.POST.get('pais_procedncia')
    das.via_transporte=request.POST.get('via_transporte')
    das.puerto_enbarque=request.POST.get('puerto_enbarque')
    das.ciudad_importador=request.POST.get('ciudad_importador')
    das.empresa_tranporte=request.POST.get('empresa_tranporte')
    das.identificacion_carga=request.POST.get('identificacion_carga')
    das.monto_flete=request.POST.get('monto_flete')
    das.total_items=request.POST.get('total_items')
    das.peso_neto=request.POST.get('peso_neto')
    das.total_bultos=request.POST.get('total_bultos')
    das.unidades_comerciales=request.POST.get('unidades_comerciales')
    das.total_tributos=request.POST.get('total_tributos')
    das.valor_seguros=request.POST.get('valor_seguros')
    das.cif=request.POST.get('cif')
    das.peso_bruto=request.POST.get('peso_bruto')
    das.unidades_fisicas=request.POST.get('unidades_fisicas')
    das.valor_fob=request.POST.get('valor_fob')
    #das.save()
    print("datos del dal gaurdados")
    cantidad=request.POST.get('cantidad')
    cant=[]
    for k in  range(int(cantidad)):
        cant.append(k)
    print(cantidad)
    mercancias=Mercancia.objects.select_related().all()
    return render (request, 'core/detalle_das.html',{'cantidad':cant,'mercancia':mercancias})
def facturaAfianzado(request):
    mercancia=request.POST.getlist('mercancia')
    advalorem=request.POST.getlist('advalorem')
    fodinfa=request.POST.getlist('fodinfa')
    iva=request.POST.getlist('iva')

    print(mercancia)
    print(advalorem)
    print(fodinfa)
    print(iva)

    das=Das.objects.last()# obtiene el utlimo dato del la consulta

    
    for i in  range(len(mercancia)):
        dD=Detalle_das()
        
        dD.mercancia=Mercancia.objects.get(id = mercancia[i])
        dD.das=das
        dD.advalorem1=advalorem[i]
        dD.fodinfa1=fodinfa[i]
        dD.iva1=iva[i]
        dD.save()
        print(i)
        fecha=Importacion.objects.last()
        afianzado=Afianzado.objects.all()
        

    return render(request,'core/factura_afianzado.html',{'fecha':fecha,'afianzado':afianzado})

def detalleAfianzado(request):
    af=Factura_afianzado()
    af.afianzado=Afianzado.objects.get(id=request.POST.get('afianzado'))
    af.importacion=Importacion.objects.get(id=request.POST.get('idfechaImport'))
    print(af.importacion.fecha)
    af.fecha=request.POST.get('fecha')
    af.numero=request.POST.get('numero')
    af.subtotal=request.POST.get('subtotal')
    #af.save()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$guardada factura afinazado guardado")
    

    
    afz=Factura_afianzado.objects.last()
    
    cant=[]
    for k in  range(4):
        cant.append(k)
      

    return render(request,'core/detalle_afianzado.html',{'cantidad':cant, 'afz':afz})


def detalleImportacion(request):
    af=request.POST.getlist('id_afianzado')
    print("················ ", af)
    desc=request.POST.getlist('descripcion')
    ape=request.POST.getlist('alpeso')
    apr=request.POST.getlist('alprecio')
    iv=request.POST.getlist('iva')
    t=request.POST.getlist('total')
    print(t)

    for i in  range(len(af)):
        dA=Detalle_afianzado()
        dA.factura_afianzado=Factura_afianzado.objects.get(id=af[0])
        dA.descripcion=desc[i]
        dA.al_peso=ape[i]
        dA.al_precio=apr[i]
        dA.iva=iv[i]
        dA.t=t[i]
      
        dA.save()


        # product=conexionApiWoo()
    print("=================")
    #print(product)
    productos=Producto.objects.select_related().all()
    proveedores=Proveedor.objects.select_related().all()
    mercancias=Mercancia.objects.select_related().all()
    # print(proveedores[0].nombre)
    # print(mercancias[2].nombre)
    
    productos=Producto.objects.all()
    for producto in productos:
        print(producto.mercancia)
       
        

    return render(request,'core/detalle_importacion.html',{"productos":productos,"proveedores":proveedores,"mercancias":mercancias})