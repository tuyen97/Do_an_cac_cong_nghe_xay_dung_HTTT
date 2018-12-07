# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from . import models
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth import logout
from django.contrib.auth import login
from .security.MyBackend import MyBackend
from django.core.paginator import Paginator
from django.core.serializers import serialize
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
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
    paginator = Paginator(products, 8)  # Show 25 contacts per page
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
        l = {
            product_id:1
        }
        request.session['cart'] = l
    else:
        cart_list = request.session['cart']
        if product_id in cart_list.keys():
            cart_list[product_id]+=1
        else:
            cart_list[product_id] = 1
        request.session['cart'] = cart_list
    print(request.session['cart'])
    http_response = {
        'status':'success',
        'message':'Thêm vào giỏ hàng thành công'
    }
    return JsonResponse(http_response)

def view_cart(request):
    if not 'cart' in request.session or not request.session['cart']:
        return HttpResponse('You don\'t have any item in cart')
    cart_list = request.session["cart"]
    cart_list_id = request.session["cart"].keys()
    items = []
    count_item = []
    sub_total = []
    for i in cart_list_id:
        product = models.Product.objects.get(pk=i)
        count_item.append(cart_list[i])
        items.append(product)
        sub_total.append(cart_list[i]*product.price)
    context = {
        'product_list': zip(items, count_item, sub_total),
        'total': sum(sub_total)
    }
    return render(request,'bakery_store/cart.html',context)

def delete_product_on_cart(request):
    id = request.POST['id']
    cart_list = request.session['cart']
    del cart_list[id]
    request.session['cart'] = cart_list
    http_response = {
        'status':'success',
        'message':'Xóa sản phẩm thành công'
    }
    return JsonResponse(http_response)

def change_quantity_on_cart(request):
    id = request.POST['id']
    count = request.POST['count']
    cart_list_id = request.session["cart"].keys()
    cart_list = request.session['cart']
    cart_list[id] = int(count)
    request.session['cart'] = cart_list
    sub_total = []
    for i in cart_list_id:
        product = models.Product.objects.get(pk=i)
        sub_total.append(cart_list[i] * product.price)
    http_response={
        'message':'Sửa số lượng thành công',
        'total':sum(sub_total)
    }
    return JsonResponse(http_response)

def checkout(request):
    form = forms.checkoutForm()
    cart_list = request.session["cart"]
    cart_list_id = request.session["cart"].keys()
    items = []
    count_item = []
    sub_total = []
    product_list=[]
    for i in cart_list_id:
        product = models.Product.objects.get(pk=i)
        product_list.append(product)
        count_item.append(cart_list[i])
        items.append(product)
        sub_total.append(cart_list[i]*product.price)
    context = {
        'product_list': zip(items, count_item, sub_total),
        'total': sum(sub_total)
    }
    paypal_dict = {
        "business": "nguyentrongtuyen15197-facilitator@gmail.com",
        "amount": sum(sub_total)/100000,
        "item_name": "Thanh toán",
        "invoice": "ạbcd",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('order_complete')),
        # "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    paypalform = PayPalPaymentsForm(initial=paypal_dict)
    if request.method == 'POST':
        f = forms.checkoutForm(request.POST)
        if f.is_valid():
            hoten = f.cleaned_data['hoten']
            diachi = f.cleaned_data['diachi']
            sdt = f.cleaned_data['sdt']
            created_date = timezone.now()
            total = sum(sub_total)
            bill = models.Bill(
                created_date=created_date,
                total=total,
                receiver_name=hoten,
                receiver_address=diachi,
                receiver_phone=sdt
            )
            bill.save()
            for i in range(len(product_list)):
                billdetail = models.BillDetail(
                    product_id=product_list[i],
                    quantity=count_item[i],
                    total=sub_total[i],
                    bill_id =bill
                )
                billdetail.save()
            request.session.pop("cart")
            return redirect('order_complete')
        else:
            context['form'] = f
            context['paypal'] = paypalform
            return render(request,'bakery_store/checkout.html',context)
    context['form'] = form
    context['paypal'] = paypalform
    return render(request,'bakery_store/checkout.html',context)

def order_complete(request):
    return render(request, 'bakery_store/order-complete.html')

@login_required()
def admin_index(request):
    return render(request, 'admin/index.html')

def ProductsIndex(request):
    list_product = models.Product.objects.filter(is_deleted=False)
    return render(request, 'admin/product/index.html',{'product_list':list_product})

def GetListProducts(request):
    list_product = models.Product.objects.all()
    products = serialize('json', list_product, cls=LazyEncoder)
    return JsonResponse(products, safe=False)

def edit_product(request):
    if request.method == 'GET':
        product = models.Product.objects.get(pk=request.GET['id'])
        form = forms.editProduct(instance=product)
        context={
            "product":product,
            'form':form
        }
        return render(request,"admin/product/edit.html", context)
    else:
        if request.method == 'POST':
            product = models.Product.objects.get(pk=request.POST['product_id'])
            form = forms.editProduct(request.POST,files=request.FILES,instance=product)
            if form.is_valid():
                form.save()
                return redirect('/admin/product')
            else:
                context = {
                    "product": product,
                    'form': form
                }
                return render(request, "admin/product/edit.html", context)
        # http_response = {
        #     'status':'success',
        #     'message':'Cap nhat thanh cong'
        # }
        # return JsonResponse(http_response)

def deleteProduct(request):
    product_id = request.POST['id']
    product = models.Product.objects.get(pk=product_id)
    product.is_deleted = True
    product.save()
    http_response = {
        'message':'Xóa sản phẩm thành công'
    }
    return JsonResponse(http_response)

def billIndex(request):
    billList = models.Bill.objects.all()
    return render(request,'admin/bill/index.html',{'billList':billList})

def billDetail(request):
    bill_id = request.GET['bill_id']
    bill = models.Bill.objects.get(pk=bill_id)
    bill_detail = models.BillDetail.objects.filter(bill_id=bill_id)
    context = {
        'bill':bill,
        'entries':bill_detail
    }
    print("ok")
    return render(request, 'admin/bill/detail.html',context)