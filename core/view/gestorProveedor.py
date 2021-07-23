from core.view.gestorImportacion import importacion
from ..controlador import saveFacuturaProveedor, saveDas
from django.shortcuts import render, redirect
from ..models import Das, Importacion,Mercancia,Factura_proveedor,Proveedor

def startFactProve(request,id):

    if request.method=='POST':
        print("estoy dentro del metodo post")

        idf=Factura_proveedor.objects.filter(importacion=id)
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

        idfp=[]
        for i in range(len(idf)):
            
            idfp.append(idf[i].id)
            
        print("el vector resultante es  ",idfp)
        respuesta=saveFacuturaProveedor(idfp,prove,id,ncajas,v_envio,v_factura,comis_envio,comis_tarjeta,isd,t_pago,extra)
        print("el das esncontrado es ")
        print()
        da=Das.objects.filter(importacion=id).first()
       
        
        if da!=None:
            idas=da.id
            return redirect ('datosdas',id,idas)
        else:
            return redirect ('startdas',id)
                
    else:
        fp=Factura_proveedor.objects.filter(importacion=id)
        proveedores=Proveedor.objects.select_related().all()
        cant=""
        for i in range(len(fp)):
            print("el tamaño de ñ cantidad es ",fp[i].id)
            cant=cant+str(fp[i].id)+";"

        datos={"id":id,
            "proveedores":proveedores,
            "cantidad":fp,
            "cant":len(fp),
            "cant":cant}
    return render(request,'core/proveedor.html',datos)


def facturaProveedor(request):
    
    # fechaImport=request.POST.get('idfechaImport')
    # #fc=Importacion.objects.get(id = 365)
    # prove= request.POST.getlist('proveedor')
    # print("valor de proveedor",prove)
    # ncajas=request.POST.getlist('ncajas')
    # v_envio=request.POST.getlist('v_envio')
    # v_factura=request.POST.getlist('v_factura')
    # comis_envio=request.POST.getlist('comis_envio')
    # comis_tarjeta=request.POST.getlist('comis_tarjeta')
    # isd=request.POST.getlist('isd')
    # t_pago=request.POST.getlist('t_pago')
    # extra=request.POST.getlist('extra')
    # print(type(ncajas))
    # respuesta=saveFacuturaProveedor(prove,fechaImport,ncajas,v_envio,v_factura,comis_envio,comis_tarjeta,isd,t_pago,extra)
    # if respuesta['error'] is True:
    #     print("·········##############")

    #     return redirect(request,'importacion')
    
    
    fecha=Importacion.objects.last()
    
    #print(context)
    return render(request,'core/das.html',{'fecha':fecha})



# def facturaProveedor(request):
#     form=FormFacturaProveedor()
#     context={
#                 'form':form
#             }
#     return render(request,'core/proveedor.html',context)

# def saveFacturaProveedor(request):
#     if request.method=='POST':
#         form=FormFacturaProveedor(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Se ha registrado correctamente!')
#             return render(request,'core/das.html')
#         else: 
#             messages.success(request, 'No se ha registrado correctamente!')
#             return redirect(request,'facturaProveedor')
#     return redirect(request,'facturaProveedor')
    