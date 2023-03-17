from django.template import Library
import math
from main.models.product import Product
register = Library()

@register.filter(name="is_in_cart")
def is_in_cart(cart,product):
    cart=list(cart.keys())
    for i in cart:
        if str(i) == str(product):
            return True

@register.filter(name="cart_count")
def cart_count(cart,product):
    product=int(product)
    old_cart=cart
    cart=cart.keys()
    for i in cart:
        if int(i) == product:
            a=str(i)
            return old_cart.get(a)
        
@register.filter(name='total_cart_count')
def total_cart_count(cart):
    cart = cart.values()
    if cart is None:
        totol_cart_count_here=0
    totol_cart_count_here = sum(cart)
    return totol_cart_count_here 


@register.filter(name='rupee_symbol')
def rupee_symbol(value):
    return f'₹ {value}'


@register.simple_tag(name='finalprice')
def finalprice(id,price,discount):
    object = Product.objects.get(id = id)
    finalprice = int(price) - int(price)*int(discount)*1/100
    object.finalprice = finalprice
    object.save()
    return finalprice


@register.filter(name="total_price")
def total_price(product,cart):
    price = int(product.finalprice)
    # print(price,'qaz',type(price))
    product=int(product.id)
    old_cart=cart
    cart=cart.keys()
    list1 = []
    for i in cart:
        if int(i) == product:
            a=str(i)
            quantity= int(old_cart.get(a))
            # print('wsx',quantity,type(quantity))
            output = price * quantity
            list1.append(output)
            # print(output,type(output))
            return output
       
       
       
@register.simple_tag(name='total_cart_price')
def total_cart_price(products , cart,request):
    sum = 0 
    for p in products:
        sum += total_price(p , cart)
    request.session['orderprice']=sum
    return sum 



#originaltotal price

@register.filter(name="total_product_originalprice")
def total_product_originalprice(product,cart):
    price = int(product.price)
    # print(price,'qaz',type(price))
    product=int(product.id)
    old_cart=cart
    cart=cart.keys()
    list1 = []
    for i in cart:
        if int(i) == product:
            a=str(i)
            quantity= int(old_cart.get(a))
            # print('wsx',quantity,type(quantity))
            output = price * quantity
            list1.append(output)
            # print(output,type(output))
            return output
       

       
@register.filter(name='total_product_price')
def total_product_price(products , cart):
    # print('hii',products)
    # print(products,cart)
    sum = 0 
    for p in products:
        sum += total_product_originalprice(p , cart)
    return sum 





@register.simple_tag(name='price_storing_in_session')
def price_storing_in_session(cart,request):
    cart = cart
    id_list = list(cart.keys())
    print(id_list)
    products = Product.objects.filter(id__in=id_list)
    print(products)
    sum = 0
    for i in products:
        print(i.id)
        quantity = cart.get(str(i.id))
        print(quantity)
        if quantity is not None:
            sum += i.finalprice * int(quantity)
    request.session['orderprice'] = sum
    print(sum)
    return 'Done'