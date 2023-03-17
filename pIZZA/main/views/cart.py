from django.shortcuts import render,redirect
from main.models.product import Product 
from main.models.category import Category
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
import razorpay
from main.models.orders import Orders
import math
from django.conf import settings
from accounts.models.user import User

class Cart(View):
    def get(self, request, *args, **kwargs):
        # Get the cart and order price data from the session
        cart = request.session.get('cart')
        keys = list(cart.keys())
        price = request.session.get('orderprice')
        
        # If the order price is not set, set it to a default value of 100
        if price is 0:
            price = int(1)

        # Get the list of product IDs from the cart and filter the Product objects accordingly
        ids = list(cart.keys())
        products = Product.objects.filter(id__in=ids)
        
        # Create a Razorpay client and generate a payment order
        client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))
        print(client,'gfsfs')
        data = { "amount": price*100, "currency": "INR", "receipt": "order_rcptid_11",'payment_capture':'1'}
        payment = client.order.create(data=data)
        
        # Debugging statement to print the payment object
        print(payment, '<<<<<<<<<<<>>>>>>>>>>>>>')
        
        # Creating order
        try:
            razorpay_order_id = request.GET.get('razorpay_order_id')
            razorpay_payment_id = request.GET.get('razorpay_payment_id')
            razorpay_signature = request.GET.get('razorpay_signature')
            email = request.session.get('email')
            user = User.objects.get(email = email)
            print(user,type(user))
        except Exception as e:
            print(e)
        if razorpay_order_id and razorpay_payment_id and razorpay_signature is not None:
            order = Orders.objects.create(user=user,
                                        #   product=list(cart.keys()),
                                          price=data['amount'],
                                          quantity=sum(list(cart.values())),razorpay_order_id=razorpay_order_id,razorpay_payment_id=razorpay_payment_id,razorpay_payment_signature=razorpay_signature)
            order.product.set(Product.objects.filter(id__in=keys))
            request.session['cart']={}
            print(order)
            return HttpResponseRedirect(request.path_info)
        
        # Add the products and payment object to the context and render the template
        context = {'products': products, 'payment': payment}
        return render(request, 'main/cart.html', context)


    
    def post(self, request, *args, **kwargs):
        # Get the values from the POST request
        delete = request.POST.get('delete')
        id = request.POST.get('id')
        remove = request.POST.get('remove')
        
        # Get the product and cart data from the session
        try:
            ptds = Product.objects.get(id=id)
        except Exception as e:
            print(e)
        orderprice = request.session.get('orderprice')
        cart = request.session.get('cart')

        # If the delete button was clicked, remove the item from the cart
        if delete is not None:
            quantity = cart.get(delete)
            orderprice = orderprice - Product.objects.get(id=delete).finalprice * quantity
            request.session['orderprice']=orderprice
            cart.pop(delete)
            request.session['cart'] = cart
            messages.success(request, 'Item deleted successfully')
            return HttpResponseRedirect(request.path_info)
        
        # If the remove button was clicked, update the order price
        # and remove one item from the cart
        if remove:
            orderprice -= ptds.finalprice
            request.session['orderprice'] = orderprice
            quantity = cart.get(id)
            if quantity:
                if quantity <= 1:
                    cart.pop(id)
                    messages.success(request, 'Item removed from cart')
                    return HttpResponseRedirect(request.path_info)
                cart[id] = quantity - 1
                request.session['cart'] = cart
                messages.success(request, 'Item removed from cart')
                return HttpResponseRedirect(request.path_info)
                
        # If the add button was clicked, update the order price
        # and add one item to the cart
        quantity = cart.get(id)
        if quantity:
            cart[id] = quantity + 1
        else:
            cart[id] = 1
        request.session['cart'] = cart
        orderprice += ptds.finalprice
        request.session['orderprice'] = orderprice
        messages.success(request, 'Item added to cart')
        return HttpResponseRedirect(request.path_info)
        

    # def get(self, request, *args, **kwargs):
    #     print(request.session.items())
    #     cart = request.session.get('cart')
    #     price = request.session.get('orderprice')
    #     if price is None:
    #         price = 100
    #     else:
    #         price = price
    #     ids = list(cart.keys())
    #     products = Product.objects.filter(id__in=ids)
    #     client = razorpay.Client(auth=("rzp_test_VSSUeyvAWk3DAu", "SiZpbqWbw9Cniuo6vpsfHQcr"))
    #     data = { "amount": price, "currency": "INR", "receipt": "order_rcptid_11" }
    #     payment = client.order.create(data=data)
    #     print(payment,'<<<<<<<<<<<>>>>>>>>>>>>>')
    #     context={'products':products,'payment':payment}
    #     return render(request,'main/cart.html',context)


    # def post(self, request, *args, **kwargs):
    #     delete = request.POST.get('del')
    #     id = request.POST.get('id')
    #     remove = request.POST.get('remove')
    #     ptds = Product.objects.get(id=id)
    #     orderprice = request.session.get('orderprice')
    #     cart = request.session.get('cart')
    #     if remove:
    #         orderprice = request.session.get('orderprice')
    #         request.session['orderprice']=orderprice-ptds.finalprice
    #     request.session['orderprice']=orderprice+ptds.finalprice
    #     quantity=cart.get(id)
    #     if quantity:
    #         if remove:
    #             if quantity<=1:
    #                 cart.pop(id)
    #                 request.session['cart']=cart
    #                 messages.success(request,'Added to cart')
    #                 return HttpResponseRedirect(request.path_info)
    #             cart[id]=quantity-1
    #             request.session['cart']=cart
    #             messages.success(request,'Added to cart')
    #             return HttpResponseRedirect(request.path_info)
    #         cart[id]=quantity+1
    #         request.session['cart']=cart
    #         messages.success(request,'Added to cart')
    #         return HttpResponseRedirect(request.path_info)
    #     print(delete,type(delete))
    #     if delete is not None:
    #         cart = request.session.get('cart')
    #         cart.pop(delete)
    #         request.session['cart']=cart
    #         messages.success(request,'Item deleted succesfully')
    #         return HttpResponseRedirect(request.path_info)


