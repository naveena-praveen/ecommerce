
from django.shortcuts import render, redirect
from shop.models import Product
from .models import CartList, Items,Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from django.contrib.auth.models import User




def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id = request.session.create()
    return ct_id


# Add product to cart
def add_cart(request,product_id):
    prod=Product.objects.get(id=product_id)
    try:
        ct=CartList.objects.get(cart_id=c_id(request))
    except CartList.DoesNotExist:
        ct=CartList.objects.create(cart_id=c_id(request))
        ct.save()

    try:
        c_items=Items.objects.get(prodt=prod,cart=ct)
        if c_items.quan < c_items.prodt.stock:
            c_items.quan += 1
        c_items.save()
    except Items.DoesNotExist:
        c_items = Items.objects.create(prodt=prod,cart=ct,quan=1)
        c_items.save()
    print(f"Cart: {ct}, Item: {c_items}")     

    return redirect('cart')

# cart details
@login_required
def cart_details(request, tot=0, count=0, cart_items=None):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        ct_items = []
    tax = 0
    grand_total = 0

    try:
        ct = CartList.objects.get(cart_id=c_id(request))
        ct_items = Items.objects.filter(cart=ct,active=True)

        for i in ct_items:
            tot += (i.prodt.price * i.quan)
            count += i.quan

        tax = (2 * tot) / 100
        grand_total = tot + tax
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', {
        'ci': ct_items,
        't': tot,
        'cn': count,
        'tax': tax,
        'grandtotal': grand_total
    })

# Decrease quantity or delete item
def mincart(request, product_id):
    ct = CartList.objects.get(cart_id=c_id(request))
    product = Product.objects.get(id=product_id)
    try:
        cart_item = Items.objects.get(prodt=product, cart=ct)
        if cart_item.quan > 1:
            cart_item.quan -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Items.DoesNotExist:
        pass
    return redirect('cart')  
    

# Increase quantity
def inccart(request, product_id):
    ct = CartList.objects.get(cart_id=c_id(request))
    product = Product.objects.get(id=product_id)
    try:
        cart_item = Items.objects.get(prodt=product, cart=ct)
        if cart_item.quan < cart_item.prodt.stock:
            cart_item.quan += 1
            cart_item.save()
    except Items.DoesNotExist:
        Items.objects.create(prodt=product, cart=ct, quan=1)
    return redirect('cart') 

def deleteitem(request,product_id):
    ct = CartList.objects.get(cart_id=c_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = Items.objects.get(prodt=product, cart=ct)
    cart_item.delete()
    return redirect('cart')




