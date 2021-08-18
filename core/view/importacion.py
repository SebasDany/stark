
from core.view.gestorProducto import saveMercacia
from django.shortcuts import render, redirect
from ..utilidades import  crearH
from ..models import Detalle_importacion, Factura_proveedor,Importacion, Mercancia, Producto,Proveedor
from ..forms import UserRegisterForm, ProductRegister
from django.contrib import messages
import datetime

id_w=[]
id_w.append(1)
precio_compra=[]
precio_neto=[]
variacion =[]
parent_id=[]
imagen=[]
categorias=[]
observaciones=[]
#saveProducto(mercan,id_w,sku,nombre,precio_compra,precio_neto,variacion,parent_id,categorias,imagen) #crear productos

def startImport(request):
    imp=Importacion(fecha=str(datetime.datetime.today()).split()[0],descripcion="",tipo="",origen="",estado=0)
    imp.save()
    
    if len(Mercancia.objects.all())==0:
        por_advalorem=[0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        subpartida=['8542390000','9031809000','9025900000', '3926909000', '8518909090', '9006910000', '8531200000', '8536419000', '8544429000', '9032891100', '8517692000', '8543709000', '8542310000', '8541900000', '8541100000', '8542900000', '8536690090', '8533319000']
        mercancia=['TARJETAS ELECTRÓNICAS','SENSORES','SENSORES MEDIDOR D', 'Carcasa De Plastico', 'Sensor De Microfono', 'PARTE DE CAMARA', 'Mini Pantalla Display', 'RELE', 'CABLES', 'REGULADORES DE VOLTAJE', 'RECEPTOR INALAMBRICO', 'KIT DE ROBOTICA', 'CIRCUITOS INTEGRADOS', 'PORTA LED', 'DIODOS', 'SOPORTE PARA TARJETAS', 'INTERRUPTORES', 'RESISTENCIAS']
        saveMercacia(mercancia,subpartida,por_advalorem) #gurada la mercancia
    id_impor=Importacion.objects.last()
    id=id_impor.id
    crearH(id,0,0,0)
    # for i in Mercancia.objects.all():
    #     #print(i.id, i.nombre)
    # for i in Producto.objects.all():
    #     print(i.id, i.nombre)
    return redirect('importacion',id)

# Create your views here.
def password(request):
    return render(request,'core/password.html')

def register(request):
    if request.method=='POST':
        print('segundo formulaei')
        form=UserRegisterForm(request.POST)
        print(form)
        pas=form['password1'].value()
        username=form['password2'].help_text
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

def importacion(request,id):
    if request.method=='POST':
        fecha=request.POST.get('fecha')
        tipo=request.POST.get('tipo')
        origen=request.POST.get('origen')
        descripcion=request.POST.get('descripcion')
       
        Importacion.objects.filter(id=id).update(fecha=fecha,descripcion=descripcion,tipo=tipo,origen=origen,)  
            
        cantidad=request.POST.get('cantidad')
        cant=[]
        proveedor=Proveedor.objects.last()
        importacion=Importacion.objects.get(id=id)
        fac=Factura_proveedor.objects.filter(importacion=id)
        if(len(fac) < int(cantidad)):
            #print(len(fac),int(cantidad))
            #print(len(fac)-int(cantidad))
        
            for k in  range(int(cantidad)-len(fac)):
                pf=Factura_proveedor(proveedor=proveedor,importacion=importacion,num_cajas=0,valor_factura=0,valor_envio=0,comision_envio=0,isd=0,total_pago=0,extra=0)  
                pf.save()
        messages.success(request, 'Se ha registrado correctamente!')
        return redirect('startFP',id)
    
    datos = Importacion.objects.get(id=id)  
    dato={"im":datos,"fecha":str(datos.fecha)}   
    return render(request,'core/importacion.html',dato)






