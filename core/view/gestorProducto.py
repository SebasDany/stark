from core.view.woocommerce import calcular, sincronizar
from core.models import Detalle_das, Detalle_importacion, Factura_proveedor, Mercancia, Proveedor
from ..controlador import  aranceles, buscarSKU, costo_unitario, costos, guardarProductoImport, incrementos, porcentuales,saveDetalleImportacion, subtotal1, subtotal2
from django.shortcuts import render, redirect
from django.http import HttpResponse
import numpy

def iniciarProduct(request):
    dtp=Detalle_importacion()
    dtp.save()


    return redirect('productosimportados')

def buscarProductos(request,id,idas,idfa):
    print("estoy denr¡ntro de crear importAIOCN")
    if request.method == 'POST':
        print("estoy denr¡ntro de crear importAIOCN")

        list_sku = request.POST.get('skus')
        
        productos=buscarSKU(list_sku,id,idas)
        datos={
                "id":id,
                "idas":idas,
                "idfa":idfa

        }
        productos.update(datos)
    return render(request, 'core/preview_productos.html',productos ) 
        
       
        
        
    
def addProductImport(request,id,idas,idfa):
    if request.method=='POST':
        if "id_producto" in request.POST:
            sku=request.POST.getlist('id_producto')
            print(sku)
            guardarProductoImport(sku,id)

    

    return redirect('viewproduct',id,idas,idfa)

def viewProduct(request,id,idas,idfa):
    pr=Detalle_importacion.objects.filter(importacion=id)
 
    proveedores=Factura_proveedor.objects.filter(importacion=id).distinct()
    # print(len(proveedores))
    # prov=[]
    # for i in range(len(proveedores)):
    #     prov.append(proveedores[i].proveedor.id)

    # unicos=numpy.unique(prov)
    # print( numpy.unique(prov))
    # h=[]
    # for j in range(len(prov)-1):
    #     print(unicos[j])
    #     k=Proveedor.objects.get(id=unicos[j])
    #     h.append(k)

    mercancias=Detalle_das.objects.filter(das=idas)
    datos={
                "id":id,
                "idas":idas,
                "idfa":idfa,
                'error':False,
            "productos":pr,
           
            "proveedores":proveedores,
            "mercancias":mercancias
        }
    return render(request, 'core/crear_importacion.html', datos ) 

def productosImportados(request,id,idas,idfa):
    if request.method=='POST':
        
        product_id=request.POST.getlist('id_producto')  
        id_df=request.POST.getlist('id_df') 
        print(product_id)
        print(id_df)
        precio=request.POST.getlist('precio')
        proveedor=request.POST.getlist('proveedor')
        cantidad=request.POST.getlist('cantidad')
        
        mercancia=request.POST.getlist('mercancia')
        peso=request.POST.getlist('peso')
        vector=numpy.zeros(len(product_id))
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector)
        subtotal=subtotal2(id)
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"],vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector,vector)
        arancel=aranceles(id)
        print(arancel["advalorem"])
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],vector,vector,vector,vector,vector,vector,vector,vector,vector)
        porcent=porcentuales(id)
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], vector,vector,vector,vector, vector,vector)
        costo=costos(id)
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], costo["costo1"],costo["costo2"],costo["costo3"],vector,vector,vector)
        costo_unit=costo_unitario(id)
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], costo["costo1"],costo["costo2"],costo["costo3"],costo_unit,vector,vector)
        incremento=incrementos(id)
        saveDetalleImportacion(id,id_df,peso,precio,cantidad,product_id,mercancia,proveedor,subtotal["Subtotales2"], arancel["advalorem"],arancel["fodinfa"],arancel["iva"],porcent["ps"],porcent["pr"],porcent["prT"], costo["costo1"],costo["costo2"],costo["costo3"],costo_unit, incremento["inc_porcentual"],incremento["inc_dolares"] )
        pr=Detalle_importacion.objects.filter(importacion=id)
        
        
        proveedores=Factura_proveedor.objects.filter(importacion=id)
        mercancias=Mercancia.objects.select_related().all()
        datos={
                "id":id,
                "idas":idas,
                "idfa":idfa,
                'error':False,
            "productos":pr,
        
            "proveedores":proveedores,
            "mercancias":mercancias
        }
        
        

        return render(request, 'core/resultados.html',datos  )
    sincronizar(id)
       
    return HttpResponse("<h1>Productos actualizados correctamente</h>")