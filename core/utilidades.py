
from .models import Historial, Producto, Detalle_importacion,Importacion

def updateEstado(id, estado):
    Importacion.objects.filter(id=id).update(estado=estado)
    return 1
def crearH(id,idas,idaf,estado):
    h=Historial()
    #h.impor=Importacion.objects.get(id=id)
    h.importacion=Importacion.objects.get(id=id)
    h.das=idas
    h.afianzado=idaf
    h.estado=estado
    h.save()
def updateH(id,idas,idaf,estado):
    h=Historial.objects.get(importacion=id)

    Historial.objects.filter(id=h.id).update(das=idas,afianzado=idaf,estado=estado)

def updateIdWooProduct( idProd, idwoo,parenId):
    Producto.objects.filter(id=idProd).update(id_woocommerce=idwoo,parent_id=parenId)

def updateCost_Invent(id_dt, new_cost, t_invet ):   
    Detalle_importacion.objects.filter(id=id_dt).update(nuevo_costo=new_cost, total_inventario=t_invet)

def updateActualizacionTienda(id_dt, estado):
    Detalle_importacion.objects.filter(id=id_dt).update(actualizado=estado)

    

