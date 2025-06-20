
from django.shortcuts import render, redirect
from shop.models import Product
from .models import CartList, Items,Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from django.contrib.auth.models import User
from accounts.models import Address
from .forms import AddressForm
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib import messages

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
    payment = None 

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
    user=request.user
    has_address =Address.objects.filter(user=user).exists()
    return render(request, 'cart.html', {
        'ci': ct_items,
        't': tot,
        'cn': count,
        'tax': tax,
        'grandtotal': grand_total,
        'has_address':has_address
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

def manual_address(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        house_no = request.POST.get('house_no')
        area = request.POST.get('area')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')

        # Save this to your Address model
        Address.objects.create(
            user=request.user,
            full_name=full_name,
            house_no=house_no,
            area=area,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone
        )
        return redirect('razorpay_checkout')  
    

def razorpay_payment(request):
    user = request.user
    tot = 0
    tax = 0
    grand_total = 0

    try:
        cart = CartList.objects.get(cart_id=c_id(request))
        cart_items = Items.objects.filter(cart=cart, active=True)

        for item in cart_items:
            tot += item.prodt.price * item.quan

        tax = (2 * tot) / 100
        grand_total = tot + tax
    except CartList.DoesNotExist:
        return redirect('cart')  # No cart

    # Razorpay expects amount in paise
    amount_paise = int(grand_total * 100)

    # Initialize Razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    payment = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': grand_total,
        'user': user,
        'cart_items': cart_items,
        'total': tot,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'checkout.html', context)

@login_required
def order_success(request):
    # Clear cart after successful payment
    try:
        cart = CartList.objects.get(cart_id=c_id(request))
        cart.delete()  # This will delete cart and all related items if on_delete=CASCADE
    except CartList.DoesNotExist:
        pass

    messages.success(request, "Your order was placed successfully!")
    return render(request, 'order_success.html')