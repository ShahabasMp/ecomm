from django.shortcuts import render,redirect
from django.views import View
from ecomapp.forms import UserRegister,UserLogin,CartForm,OrderForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Products,Carts,Orders
from django.core.mail import send_mail,settings
# Create your views here.
class HomeView(View):
    def get(self,request,*args,**kwargs):
        data=Products.objects.all()
        return render(request,'index.html',{'products':data})
    
class UserRegisterView(View):
    def get(self,request,*args,**kwargs):
        form=UserRegister()
        return render(request,'user_register.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=UserRegister(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,'Registration successfull')
            return redirect('log_view')
        else:
            messages.error(request,'invalid')
            return redirect('home_view')

class UserLoginView(View):
    def get(self,request):
        form=UserLogin()
        return render(request,'user_login.html',{'form':form})
    def post(self,request):
        psw=request.POST.get('password')
        uname=request.POST.get('username')
        user=authenticate(request,username=uname,password=psw)
        if user:
            login(request,user)
            messages.success(request,'Login Successfull')
            return redirect('home_view')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('log_view')
        
class UserLogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'Logout successfull')
        return redirect('home_view')
    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        return render(request,'product_detail.html',{'product':product})
    
class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        form=CartForm()
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        return render(request,'addtocart.html',{'form':form,'product':product})
    
    def post(self,request,*args,**kwargs):
        u=request.user
        id=kwargs.get('id')
        p=Products.objects.get(id=id)
        q=request.POST.get('quantity')
        Carts.objects.create(user=u,quantity=q,product=p)
        return redirect('home_view')


class CartListView(View):
    def get(self,request,*args,**kwargs):
        data=Carts.objects.filter(user=request.user).exclude(status='order-placed')
        return render(request,'cartlist.html',{'data':data})

class PlaceOrderView(View):
    def get(self,request,*args,**kwargs):
        form=OrderForm()
        return render(request,'place-order.html',{'form':form})
    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get('cart_id')
        cart=Carts.objects.get(id=cart_id)
        user=request.user
        address=request.POST.get('address')
        email=request.POST.get('email')
        Orders.objects.create(user=user,cart=cart,address=address,email=email)
        send_mail("confirmation","order placed successfully!",settings.EMAIL_HOST_USER,[email])
        cart.status='order-placed'
        cart.save()
        return redirect('home_view')

class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        data=Carts.objects.get(id=id)
        data.delete()
        return redirect('cartlist_view')






