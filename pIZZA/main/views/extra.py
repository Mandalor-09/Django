from django.shortcuts import render,redirect
from main.models.product import Product 
from main.models.category import Category
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse

def service(request, *args, **kwargs):
    return render(request,'main/services.html')


def about(request, *args, **kwargs):
    return render(request,'main/about.html')


def contact(request, *args, **kwargs):
    return render(request,'main/contact.html')


def blog(request, *args, **kwargs):
    return render(request,'main/blog.html')