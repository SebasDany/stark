from django.urls import path
from . import views
from django.contrib.auth import login ,logout
urlpatterns = [
    path('',views.login,name='login'),
    
]