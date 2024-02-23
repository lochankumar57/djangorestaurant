from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('login',views.login,name="login"),
    path('reg',views.reg,name="reg"),
    path('menu',views.menu,name="menu"),
    path('signout',views.signout,name="signout"),
    path('manage',views.manage,name="manage"),
    path('payments',views.payments,name="payments"),
    path('conforder',views.conforder,name="conforder"),
    path('ratings',views.ratings,name="ratings"),

]