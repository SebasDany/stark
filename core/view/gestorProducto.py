
from core.models import Mercancia, Producto

## Función para guardar la mercancia
def saveMercacia(mer=[],sub=[],adv=[]):
    print(len(mer))
    print(len(sub))
    print(len(adv))
    for i in range(len(mer)):
        print(mer[i])
        m=Mercancia()
        m.nombre=mer[i]
        m.subpartida=sub[i]
        m.por_advalorem=adv[i]
        m.save()

## Funcion de guardar productos

def saveProducto(mercancia=[],id_wo=[],sku=[],nombre=[],precio_compra=[],precio_neto=[],variacion =[],
parent_id=[],imagen=[],categorias=[],observaciones=[]):

    for i in range(len(mercancia)):
        pr=Producto()
        pr.mercancia=Mercancia.objects.get(nombre=mercancia[i])
        pr.id_woocommerce=2
        pr.sku=sku[i]
        pr.nombre=nombre[i]
        pr.precio_compra=45.0
        pr.precio_neto=50.5
        pr.variacion=1
        pr.parent_id=3
        pr.imagen="djsfjdnjfndjn.jpg"
        pr.categorias=mercancia[i]
        pr.observaciones="descripcion del producto"
        pr.save()
