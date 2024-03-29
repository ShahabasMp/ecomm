from django import forms
from django.contrib.auth.models import User
from ecomapp.models import Carts,Orders

class UserRegister(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),
            'password':forms.TextInput(attrs={'class':'form-control','placeholder':'Password'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),


        }

class UserLogin(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={
            'password':forms.TextInput(attrs={'class':'form-control','placeholder':'Password'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'User name'}),

        }

class CartForm(forms.ModelForm):
    class Meta:
        model=Carts
        fields=['quantity']

        widgets={
            'quantity':forms.NumberInput(attrs={'class':'form-control'})
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model=Orders
        fields=['address','email']
        widgets={
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }
