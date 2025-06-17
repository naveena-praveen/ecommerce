import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import Address
from .forms import AddressForm

from .forms import EmailForm, OTPForm

def email_login(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = str(random.randint(100000, 999999))
            
            # Store in session
            request.session['email'] = email
            request.session['otp'] = otp

            # Send OTP via email
            send_mail(
                'Your OTP for Login',
                f'Use this OTP to login: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('verify_otp')
    else:
        form = EmailForm()
    
    return render(request, 'email_login.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_otp = request.session.get('otp')
            email = request.session.get('email')

            if entered_otp == session_otp:
                # Get or create user with that email
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={'username': email.split('@')[0]}
                )
                login(request, user)
                messages.success(request, "Login successful!")
                
                # Clear session
                request.session.pop('otp', None)
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP')
    else:
        form = OTPForm()
    
    return render(request, 'verify_otp.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/address_list.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if not Address.objects.filter(user=request.user).exists():
                address.is_default = True  # first address = default
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Edit'})