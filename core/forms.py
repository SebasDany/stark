from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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