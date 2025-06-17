from django import forms
from .models import Address

class EmailForm(forms.Form):
      email=forms.EmailField()
      widget=forms.EmailInput(attrs={
           'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True,
      })
  
    
class OTPForm(forms.Form):
    otp=forms.CharField(max_length=6) 
    widget=forms.EmailInput(attrs={
           'class': 'form-control',
            'placeholder': 'OTP',
            'required': True,
      })


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'full_name', 'phone', 'house_no', 'area', 'city', 'state', 'pincode'
        ]
        
        widget=forms.EmailInput(attrs={
           'class': 'form-control',
            'placeholder': 'OTP',
            'required': True,
            })
      