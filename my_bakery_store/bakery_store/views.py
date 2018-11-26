# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from . import models
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth import logout
from django.contrib.auth import login
from .security.MyBackend import MyBackend
from django.core.paginator import Paginator
from django.core.serializers import serialize
# Create your views here.
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)


def index(request):
    if request.user.is_authenticated:
        print(request.user.role)
        if request.user.role == 'ad\n':
            return redirect('/admin')

    products = models.Product.objects.all()
    paginator = Paginator(products, 3)  # Show 25 contacts per page
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    context = {
        'product_list':product_list,
        'paginator': paginator
    }
    return render(request,'bakery_store/shop.html',context)

def register(request):
    form = forms.registerForm()
    if request.method == "POST":
        f = forms.registerForm(request.POST, request.FILES)
        if f.is_valid():
            print(f.cleaned_data['user_name'])
            print(f.cleaned_data['password'])
            f.save()
            return HttpResponse('success')
        else:
            return render(request,"bakery_store/register.html",{'form':f})
    else:
        return render(request,"bakery_store/register.html",{'form':form})

def Logout(request):
    logout(request)
    return redirect('/')

def loginView(request):
    logout(request)
    if request.method == 'GET':
        context = {
            'form': forms.loginForm()
        }
        return render(request, 'bakery_store/login.html', context)
    if request.method == 'POST':
        f = forms.loginForm(request.POST)
        if(f.is_valid()):
            user_name = f.cleaned_data['user_name']
            password = f.cleaned_data['password']
            user = MyBackend().authenticate(user_name=user_name,password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                print("user is logged in")
                     # request.session['user_name']=user.user_name
                     # request.session['user_avt'] = user.avt.url
                if user.role=='mem':
                    return redirect('/')
                else:
                    return redirect('/admin')
            else:
                return HttpResponse("Login fail")
        else:
            return render(request,'bakery_store/login.html',{'form':f})

@login_required()
def add_product(request):
    form = forms.productForm()
    if request.method == 'POST':
        f = forms.productForm(data=request.POST, files=request.FILES)
        if(f.is_valid()):
            f.save()
            return HttpResponse("success")
        else:
            return render(request, "admin/add_product.html",{'form':f})
    else:
        return render(request,"admin/add_product.html",{"form":form})


def product_detail(request):
   # print(request.session['user_avt'])
    product = models.Product.objects.get(pk=request.GET['id'])
    context={
        "product":product
    }
    return render(request, "bakery_store/product_detail.html",context)

def add_to_cart(request):
    product_id = request.POST['id']
    if not 'cart' in request.session or not request.session['cart']:
        request.session['cart'] = [product_id]
    else:
        cart_list = request.session['cart']
        cart_list.append(product_id)
        request.session['cart'] = cart_list
    print(set(request.session['cart']))
    http_response = {
        'status':'success',
        'message':'Thêm vào giỏ hàng thành công'
    }
    return JsonResponse(http_response)

def view_cart(request):
    product_list = []
    if not 'cart' in request.session or not request.session['cart']:
        return HttpResponse('You don\'t have any item in cart')
    cart_list = set(request.session["cart"])
    for id in cart_list:
        product = models.Product.objects.get(pk=id)
        product_list.append(product)
    context = {
        'product_list':product_list
    }
    return render(request,'bakery_store/cart.html',context)

def delete_product_on_cart(request):
    id = request.POST['id']
    request.session['cart'].remove(id)
    http_response = {
        'status':'success',
        'message':'Xóa sản phẩm thành công'
    }
    return JsonResponse(http_response)

@login_required()
def admin_index(request):
    return render(request, 'admin/index.html')

def ProductsIndex(request):
    return render(request, 'admin/product/index.html')

def GetListProducts(request):
    list_product = models.Product.objects.all()
    products = serialize('json', list_product, cls=LazyEncoder)
    return JsonResponse(products, safe=False)

def edit_product(request):
    if request.method == 'GET':
        product = models.Product.objects.get(pk=request.GET['id'])
        context={
            "product":product
        }
        return render(request,"admin/product/edit.html", context)
    else:
        http_response = {
            'status':'success',
            'message':'Cap nhat thanh cong'
        }
        return JsonResponse(http_response)