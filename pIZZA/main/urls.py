from django.urls import path
from main.views.home import Home
from main.views.menu import Menu
from main.views.cart import Cart
from main.views.extra import about,blog,contact,service

urlpatterns = [
    path('home',Home.as_view(),name='home'),
    path('',Home.as_view(),name='home'),
    path('menu',Menu.as_view(),name='menu'),
    path('cart',Cart.as_view(),name='cart'),
    path('about',about,name='about'),
    path('blog',blog,name='blog'),
    path('contact',contact,name='contact'),
    path('service',service,name='service'),
]
