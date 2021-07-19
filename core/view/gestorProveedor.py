from ..controlador import saveFacuturaProveedor, saveDas
from django.shortcuts import render, redirect
from ..models import Importacion,Mercancia

def facturaProveedor(request):
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
    print(type(ncajas))
    respuesta=saveFacuturaProveedor(prove,fechaImport,ncajas,v_envio,v_factura,comis_envio,comis_tarjeta,isd,t_pago,extra)
    if respuesta['error'] is True:
        print("·········##############")

        return redirect(request,'importacion')
    
    
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
    