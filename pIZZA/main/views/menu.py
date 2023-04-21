from main.models.category import Category
from main.models.product import Product,Images,Combo
from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.db import models
class Menu(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('cart'):
            cart={}
            request.session['cart']=cart
        categories = Category.objects.all()
        products = Product.objects.all()
        combos = Combo.objects.all()
        print(request.session,'<<<<<<<<>>>')
        context = {
            'categories':categories,
            'products':products,
            'combos':combos,
        }
        try:
            if request.GET.get('category') is not None:
                filtercategorys=request.GET.get('category')
                filtercategorys=Category.objects.get(slug=filtercategorys)
                filterproducts = filtercategorys.product.all()
                context['products']=filterproducts
            if request.GET.get('search') is not None:
                search_query=request.GET.get('search')
                
                filterproducts=Product.objects.filter(models.Q(name__icontains=search_query) | models.Q(detail__icontains=search_query))
                
                context['products']=filterproducts
        except Exception as e:
            print(e)
        return render(request,'main/menu.html',context=context)

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        id = request.POST.get('id')
        remove = request.POST.get('remove')
    # print('CART IS',cart)
        if cart:
            quantity = cart.get(id)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(id)
                        request.session['cart']=cart
                        messages.success(request,'Removed from Cart')
                        return HttpResponseRedirect(request.path_info)

                    cart[id]=quantity -1
                    request.session['cart']=cart
                    messages.success(request,'Removed from Cart')
                    return HttpResponseRedirect(request.path_info)
                else:    
                    cart[id]=quantity+1 
                    request.session['cart']=cart
                    messages.success(request,'Added from Cart')
                    return HttpResponseRedirect(request.path_info)
            else:
                cart[id]=1   
                request.session['cart']=cart
                messages.success(request,'Added from Cart')
                return HttpResponseRedirect(request.path_info)
        else:
            cart={}
            cart[id]=1
            request.session['cart']=cart
            # print('Product added now cart is',cart)
            messages.success(request,'Added to Cart Successfully')
            return HttpResponseRedirect(request.path_info)