from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.homepage,),

    path('register/',views.Register,name="Register"),
    path('login/',views.logn,name="login"),
    path('logout/',views.log_out,name="logout"),
    path('tables/',views.select_table,name="tables"),
    path('menu/',views.menu,name="menu"),
    path('cart/',views.cart,name="cart"),
    path('addToCart/',views.addToCart,name="addToCart"),
    path('plusCart/', views.plusCart),
    path('minusCart/', views.minusCart),
    path('removeCart/', views.removeCart),
    path('billpdf',views.bill,name="bill"),
    path('dopdf/',views.generate_pdf,name="dopdf"),
]
