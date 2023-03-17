from main.models.category import Category
from main.models.product import Product,Images,Combo
from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages

class Home(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('cart'):
            request.session['cart']={}
        categories = Category.objects.all()
        products = Product.objects.filter(is_offer = True)[0:3]
        products2 = Product.objects.filter(is_offer = True)
        combos = Combo.objects.all()
        context = {
            'categories':categories,
            'products':products,
            'combos':combos,
            'swiper_products':products2,
        }
        try:
            filtercategorys=request.GET.get('category')
            print(filtercategorys)
            filtercategorys=Category.objects.get(slug=filtercategorys)
            filterproducts = filtercategorys.product.all()[0:3]
            context['products']=filterproducts
        except Exception as e:
            print(e)
        return render(request,'main/index.html',context=context)

    def post(self, request, *args, **kwargs):
        pass