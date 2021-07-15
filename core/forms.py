from django.db import models
from django.forms import fields, widgets


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from.models import Importacion, Producto, Das,Factura_proveedor

class UserRegisterForm(UserCreationForm):
    username=forms.CharField(max_length=100)
    email=forms.EmailField()
    password1=forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        help_texts= {k:"" for k in fields }


class UserRegisterForm(UserCreationForm):
    username=forms.CharField(max_length=10)
    email=forms.EmailField()
    password1=forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
   
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        help_texts= {k:" " for k in fields }

class ProductRegister(forms.ModelForm):
    class Meta:
        model=Producto
        fields='__all__'
   
class FormImportacion(forms.ModelForm):
        class Meta:
            model=Importacion
            fields=['fecha','descripcion','tipo','origen']

class FormFacturaProveedor(forms.ModelForm):
        class Meta:
            model=Factura_proveedor
            fields='__all__'
            
class FormDas(forms.ModelForm):
        class Meta:
            model=Das
            fields='__all__'
            # fields=['numero_entrega',
            #'numero_atribuido',
            # 'fecha_embarque',
            # 'fecha_llegada',
            # 'documento_transporte',
            # 'tipo_carga',
            # 'pais_procedncia',
            # 'via_transporte',
            # 'puerto_enbarque',
            # 'ciudad_importador',
            # 'empresa_tranporte',
            # 'identificacion_carga',
            # 'monto_flete',
            # 'total_items',
            # 'peso_neto',
            # 'total_bultos',
            # 'unidades_comerciales',
            # 'total_tributos',
            # 'valor_seguros',
            # 'cif',
            # 'peso_bruto',
            # 'unidades_fisicas',
            # 'valor_fob'

            
            # ]
            
            