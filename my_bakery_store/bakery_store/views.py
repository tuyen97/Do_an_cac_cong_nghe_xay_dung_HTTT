# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from . import models
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
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
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models.functions import TruncMonth, TruncDate, TruncDay
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)

def is_admin(user):
    return user.role == 'ad'

def index(request):
    if request.user.is_authenticated:
        print(request.user.role)
        if request.user.role == 'ad':
            return redirect('/admin')

    products = models.Product.objects.filter(is_deleted=False)
    saled_pro = []
    fil_pr = []
    event = {}
    if models.Event.objects.filter(status='act').exists():
        event = models.Event.objects.filter(status='act')[0]
        applieds = models.AppliedProduct.objects.filter(event=event.id)
        for apply in applieds:
            saled_pro.append(apply.product)
        for product in products:
            if product in saled_pro:
                product.price -= int(product.price * event.sale_off/100)
                fil_pr.append(product)
            else:
                fil_pr.append(product)
    paginator = Paginator(fil_pr, 6)  # Show 25 contacts per page
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    context = {
        'product_list':product_list,
        'saled_pro':saled_pro,
        'event':event,
        'paginator': paginator
    }
    return render(request,'bakery_store/shop.html',context)

def search(request):
    query = request.GET['search']
    products = models.Product.objects.filter(Q(name__contains=query)|Q(descript__contains=query), is_deleted=False)
    saled_pro = []
    fil_pr = []
    event = {}
    if models.Event.objects.filter(status='act').exists():
        event = models.Event.objects.filter(status='act')[0]
        applieds = models.AppliedProduct.objects.filter(event=event.id)
        for apply in applieds:
            saled_pro.append(apply.product)
        for product in products:
            if product in saled_pro:
                product.price -= int(product.price * event.sale_off/100)
                fil_pr.append(product)
            else:
                fil_pr.append(product)
    paginator = Paginator(fil_pr, 8)  # Show 25 contacts per page
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    context = {
        'product_list':product_list,
        'saled_pro':saled_pro,
        'event':event,
        'paginator': paginator
    }
    return render(request,'bakery_store/shop.html',context)

def register(request):
    form = forms.registerForm()
    if request.method == "POST":
        f = forms.registerForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            user_name = f.cleaned_data['user_name']
            password = f.cleaned_data['password']
            user = MyBackend().authenticate(user_name=user_name, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                print("user is logged in")
                # request.session['user_name']=user.user_name
                # request.session['user_avt'] = user.avt.url
                return redirect('/')
        else:
            return render(request,"bakery_store/register_form.html",{'form':f})
    else:
        return render(request,"bakery_store/register_form.html",{'form':form})

def Logout(request):
    logout(request)
    return redirect('/')

def loginView(request):
    logout(request)
    if request.method == 'GET':
        context = {
            'form': forms.loginForm()
        }
        return render(request, 'bakery_store/login_form.html', context)
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
            return render(request,'bakery_store/login_form.html',{'form':f})

def product_detail(request):
   # print(request.session['user_avt'])
    product = models.Product.objects.get(pk=request.GET['id'])
    events = product.appliedproduct_set.all()
    for event in events:
        if event.event.status == 'act':
            product.price -= int(product.price * event.event.sale_off/100)
            comment_list = models.Comment.objects.filter(product=product.id)
            context = {
                'sale': event.event.sale_off,
                "product": product,
                "comment_list": comment_list
            }
            return render(request, "bakery_store/product_detail.html", context)
    comment_list = models.Comment.objects.filter(product = product.id)
    context={
        "product":product,
        "comment_list":comment_list
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
        return render(request,'bakery_store/empty_cart.html')
    cart_list = request.session["cart"]
    cart_list_id = request.session["cart"].keys()
    items = []
    count_item = []
    sub_total = []
    for i in cart_list_id:
        product = models.Product.objects.get(pk=i)
        events = product.appliedproduct_set.all()
        for event in events:
            if event.event.status == 'act':
                product.price -= int(product.price * event.event.sale_off / 100)
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
        events = product.appliedproduct_set.all()
        for event in events:
            if event.event.status == 'act':
                product.price -= int(product.price * event.event.sale_off / 100)
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
        events = product.appliedproduct_set.all()
        for event in events:
            if event.event.status == 'act':
                product.price -= int(product.price * event.event.sale_off / 100)
        product_list.append(product)
        count_item.append(cart_list[i])
        items.append(product)
        sub_total.append(cart_list[i]*product.price)
    context = {
        'product_list': zip(items, count_item, sub_total),
        'total': sum(sub_total)
    }
    if request.method == 'POST':
        f = forms.checkoutForm(request.POST)
        if f.is_valid():
            hoten = f.cleaned_data['hoten']
            diachi = f.cleaned_data['diachi']
            sdt = f.cleaned_data['sdt']
            created_date = timezone.now()
            total = sum(sub_total)
            if request.user.is_authenticated:
                bill = models.Bill(
                    created_date=created_date,
                    total=total,
                    receiver_name=hoten,
                    receiver_address=diachi,
                    receiver_phone=sdt,
                    user_id=request.user
                )
                bill.save()
            else:
                bill = models.Bill(
                    created_date=created_date,
                    total=total,
                    receiver_name=hoten,
                    receiver_address=diachi,
                    receiver_phone=sdt
                )
                bill.save()

            for i in range(len(product_list)):
                product_list[i].available_quantity -= count_item[i]
                events = product_list[i].appliedproduct_set.all()
                e = None
                for event in events:
                    if event.event.status == 'act':
                        product_list[i].price = int(product_list[i].price *100 /(100-event.event.sale_off))
                        product_list[i].save()
                        e = event.event
                if e is not None:
                    billdetail = models.BillDetail(
                        product_id=product_list[i],
                        quantity=count_item[i],
                        total=sub_total[i],
                        bill_id=bill,
                        event_id=e
                    )
                else:
                    product_list[i].save()
                    billdetail = models.BillDetail(
                        product_id=product_list[i],
                        quantity=count_item[i],
                        total=sub_total[i],
                        bill_id=bill
                    )

                billdetail.save()
            request.session.pop("cart")
            return redirect('order_complete')
        else:
            context['form'] = f
            return render(request,'bakery_store/checkout.html',context)
    context['form'] = form
    return render(request,'bakery_store/checkout.html',context)

def order_complete(request):
    return render(request, 'bakery_store/order-complete.html')

@login_required
def add_comment(request):
    user = models.User.objects.get(pk=request.POST['customer_id'])
    product = models.Product.objects.get(pk=request.POST['product_id'])
    text_content = request.POST['text_content']
    star = []
    comment = models.Comment()
    rating = request.POST['rating']
    if rating != '':
        for _ in range(int(rating)):
            star.append("x")
    else:
        star = 'xxxxx'
    comment.user = user
    comment.product = product
    comment.content = text_content
    if len(request.FILES):
        image_content = request.FILES['image_content']
        comment.image = image_content
    comment.created_date = timezone.now()
    comment.rating=''.join(star)
    comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@user_passes_test(is_admin)
def admin_index(request):
    bill_count = models.Bill.objects.filter(status='proc').count()
    product_count = models.Product.objects.filter(is_deleted=False).count()
    event_count = models.Event.objects.filter(status='pen').count()
    customer_count = models.User.objects.filter(role='mem').count()
    context = {
        'bill_count':bill_count,
        'product_count':product_count,
        'event_count':event_count,
        'customer_count':customer_count
    }
    return render(request, 'admin/index.html',context)

@user_passes_test(is_admin)
def add_product(request):
    form = forms.productForm()
    if request.method == 'POST':
        f = forms.productForm(data=request.POST, files=request.FILES)
        if(f.is_valid()):
            f.save()
            return redirect('view_product')
        else:
            return render(request, "admin/add_product.html",{'form':f})
    else:
        return render(request,"admin/add_product.html",{"form":form})

@user_passes_test(is_admin)
def ProductsIndex(request):
    list_product = models.Product.objects.filter(is_deleted=False)
    return render(request, 'admin/product/index.html',{'product_list':list_product})

@user_passes_test(is_admin)
def GetListProducts(request):
    list_product = models.Product.objects.all()
    products = serialize('json', list_product, cls=LazyEncoder)
    return JsonResponse(products, safe=False)

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
def deleteProduct(request):
    product_id = request.POST['id']
    product = models.Product.objects.get(pk=product_id)
    product.is_deleted = True
    product.save()
    http_response = {
        'message':'Xóa sản phẩm thành công'
    }
    return JsonResponse(http_response)

@user_passes_test(is_admin)
def billIndex(request):
    billList = models.Bill.objects.all()
    return render(request,'admin/bill/index.html',{'billList':billList})

@user_passes_test(is_admin)
def billDetail(request):
    form = forms.approveBill()
    bill_id = request.GET['bill_id']
    bill = models.Bill.objects.get(pk=bill_id)
    bill_detail = models.BillDetail.objects.filter(bill_id=bill_id)
    context = {
        'bill':bill,
        'entries':bill_detail,
        'form':form
    }
    print("ok")
    return render(request, 'admin/bill/detail.html',context)

@user_passes_test(is_admin)
def approveBill(request):
    bill_id  =request.POST['id']
    bill_status = request.POST['status']
    bill = models.Bill.objects.get(pk = bill_id)
    if bill_status=='fail':
        bill_details = models.BillDetail.objects.filter(bill_id=bill_id)
        for bill_detail in bill_details:
            product = bill_detail.product_id
            product.available_quantity += bill_detail.quantity
            product.save()
    bill.status = bill_status
    bill.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def loginForm(request):
    return render(request,'bakery_store/login_form.html')

@user_passes_test(is_admin)
def eventIndex(request):
    event_list = models.Event.objects.all()
    context = {
        'event_list':event_list
    }
    return render(request, 'admin/event/index.html',context)

@user_passes_test(is_admin)
@csrf_exempt
def editEventForm(request):
    if request.method == 'GET':
        event = models.Event.objects.get(pk = request.GET['id'])
        products = models.Product.objects.filter(is_deleted=False)
        applied = models.AppliedProduct.objects.filter(event=request.GET['id'])
        applied_products = []
        for i in applied:
            applied_products.append(i.product)
        # print(applied_p)
        print(';ok')
        context = {
            'products':products,
            'event':event,
            'applied_product':applied_products
        }
        return render(request, 'admin/event/edit.html',context)
    else:
        http_response = {}
        id = request.POST['id']
        product_list = request.POST.getlist("products[]")
        sale = request.POST['sale']
        event_id = request.POST['event_id']
        name = request.POST['name']
        start = datetime.datetime.strptime(request.POST['start'], '%Y-%m-%d')
        end = datetime.datetime.strptime(request.POST['end'], '%Y-%m-%d')
        today = datetime.datetime.today()
        if start < today:
            http_response['message'] = 'Vui lòng chọn sự kiện trong tưong lai'
            return JsonResponse(http_response)
        if start > end:
            http_response['message'] = 'Khoảng thời gian không hợp lệ'
            return JsonResponse(http_response)
        # if models.Event.objects.filter(event_id=event_id).exists():
        #     http_response['message'] = 'Trùng mã sự kiện'
        #     return JsonResponse(http_response)
        if models.Event.objects.filter(status='act').exists():
            active_event = models.Event.objects.filter(status='act')[0]
            active_event_start = active_event.finish_time
            if start.date() < active_event_start:
                http_response['message'] = 'Vẫn có sự kiện xảy ra trong thời gian này '
                return JsonResponse(http_response)
        event = models.Event.objects.get(pk=id)
        event.name = name
        event.event_id = event_id
        event.start_time = start
        event.finish_time = end
        event.sale_off = sale
        event.save()
        for id in product_list:
            product = models.Product.objects.get(pk=id)
            applied_p = models.AppliedProduct(event=event, product=product)
            applied_p.save()
        http_response['message'] = 'Thêm sự kiện thành công'
        return JsonResponse(http_response)

@user_passes_test(is_admin)
def eventChange(request):
    http_response = {}
    if 'ketthuc' in request.POST:
        event_id = request.POST['id']
        event = models.Event.objects.get(pk=event_id)
        event.status = 'fin'
        event.save()
        http_response['message']='Kết thúc sự kiện'
        return JsonResponse(http_response)
    if 'kichhoat' in request.POST:
        event_id = request.POST['id']
        event = models.Event.objects.get(pk=event_id)
        if models.Event.objects.filter(status='act').exists():
            # active_event = models.Event.objects.filter(status='act')[0]
            # active_event_start = active_event.finish_time
            # if event.start_time < active_event_start:
            http_response['message'] = 'Đang có sự kiện'
            return JsonResponse(http_response)
        event.status = 'act'
        event.save()
        http_response['message']= 'Kích hoạt sự kiện'
        return JsonResponse(http_response)
    if 'xoask' in request.POST:
        id = request.POST['id']
        event = models.Event.objects.get(pk=id)
        event.delete()
        http_response['message'] = 'Xóa thành công'
        return JsonResponse(http_response)

@user_passes_test(is_admin)
@csrf_exempt
def createEvent(request):
    products = models.Product.objects.filter(is_deleted=False)
    context = {
        'products':products
    }
    if request.method == 'POST':
        http_response = {}
        product_list = request.POST.getlist("products[]")
        print(product_list)
        sale = request.POST['sale']
        event_id = request.POST['event_id']
        name = request.POST['name']
        start = datetime.datetime.strptime(request.POST['start'], '%Y-%m-%d')
        end = datetime.datetime.strptime(request.POST['end'], '%Y-%m-%d')
        today = datetime.datetime.today()
        if start < today:
            http_response['message'] = 'Vui lòng chọn sự kiện trong tưong lai'
            return JsonResponse(http_response)
        if start > end:
            http_response['message'] = 'Khoảng thời gian không hợp lệ'
            return JsonResponse(http_response)
        if models.Event.objects.filter(event_id=event_id).exists():
            http_response['message'] = 'Trùng mã sự kiện'
            return JsonResponse(http_response)
        if models.Event.objects.filter(status='act').exists():
            active_event = models.Event.objects.filter(status='act')[0]
            active_event_start = active_event.finish_time
            if start.date() < active_event_start:
                http_response['message'] = 'Vẫn có sự kiện xảy ra trong thời gian này '
                return JsonResponse(http_response)
        event = models.Event()
        event.name = name
        event.event_id = event_id
        event.start_time = start
        event.finish_time = end
        event.sale_off = sale
        event.save()
        for id in product_list:
            product = models.Product.objects.get(pk=id)
            applied_p = models.AppliedProduct(event=event, product=product)
            applied_p.save()
        http_response['message'] = 'Thêm sự kiện thành công'
        return JsonResponse(http_response)
    return render(request, 'admin/event/create.html',context)

@user_passes_test(is_admin)
def statisticsProduct(request):
    if request.method == 'POST':
        range = request.POST['range']
        if range == 'day':
            product_list = []
            product_count = {}
            day = timezone.now().day
            bills = models.Bill.objects.filter(created_date__day=day)
            for bill in bills:
                billdetails = models.BillDetail.objects.filter(bill_id=bill.id)
                for billdetail in billdetails:
                    if billdetail.product_id in product_count:
                        product_count[billdetail.product_id]+= billdetail.quantity
                    else:
                        product_count[billdetail.product_id] = billdetail.quantity
            for key in product_count.keys():
                product_list.append({key.name:product_count[key]})
            response = {
                'static_list':product_list
            }
            return JsonResponse(response)
        if range == 'week':
            product_list = []
            product_count = {}
            week = timezone.now().weekday()
            print(week)
            bills = models.Bill.objects.filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(days=7))
            for bill in bills:
                billdetails = models.BillDetail.objects.filter(bill_id=bill.id)
                for billdetail in billdetails:
                    if billdetail.product_id in product_count:
                        product_count[billdetail.product_id]+= billdetail.quantity
                    else:
                        product_count[billdetail.product_id] = billdetail.quantity
            for key in product_count.keys():
                product_list.append({key.name:product_count[key]})
            response = {
                'static_list':product_list
            }
            return JsonResponse(response)
        if range == 'month':
            product_list = []
            product_count = {}
            month = timezone.now().month
            bills = models.Bill.objects.filter(created_date__month=month)
            for bill in bills:
                billdetails = models.BillDetail.objects.filter(bill_id=bill.id)
                for billdetail in billdetails:
                    if billdetail.product_id in product_count:
                        product_count[billdetail.product_id]+= billdetail.quantity
                    else:
                        product_count[billdetail.product_id] = billdetail.quantity
            for key in product_count.keys():
                product_list.append({key.name:product_count[key]})
            response = {
                'static_list':product_list
            }
            return JsonResponse(response)
        if range == 'year':
            product_list = []
            product_count = {}
            year = timezone.now().year
            bills = models.Bill.objects.filter(created_date__year= year)
            for bill in bills:
                billdetails = models.BillDetail.objects.filter(bill_id=bill.id)
                for billdetail in billdetails:
                    if billdetail.product_id in product_count:
                        product_count[billdetail.product_id]+= billdetail.quantity
                    else:
                        product_count[billdetail.product_id] = billdetail.quantity
            for key in product_count.keys():
                product_list.append({key.name:product_count[key]})
            response = {
                'static_list':product_list
            }
            return JsonResponse(response)
    return render(request, 'admin/product/statistics.html')

@login_required
def profile(request):
    return render(request, 'bakery_store/customer/profile.html')

@login_required
def customerOrders(request):
    bills = models.Bill.objects.filter(user_id=request.user)
    context ={
        'bills':bills
    }
    return render(request, 'bakery_store/customer/orders.html', context)

@login_required
def customerOrderDetail(request):
    bill_id = request.GET['id']
    bill = models.Bill.objects.get(pk=bill_id)
    bill_detail = models.BillDetail.objects.filter(bill_id=bill_id)
    context = {
        'bill': bill,
        'entries': bill_detail
    }
    # print("ok")
    return render(request, 'bakery_store/customer/order_detail.html',context)

@user_passes_test(is_admin)
@csrf_exempt
def statisticsRevenueForm(request):
    if request.method == 'POST':
        range = request.POST['range']
        if range == 'week':
            stat = models.Bill.objects.\
                filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(days=7)). \
                annotate(date=TruncDay('created_date')).\
                values('date').annotate(count = Sum('total')).all()
            resp = []
            for i in stat.iterator():
                # print(i)
                resp.append({
                    str(i['date']):i['count']
                })
            return JsonResponse({'static_list':resp})
        if range == 'month':
            month = timezone.now().month
            stat = models.Bill.objects. \
                filter(created_date__month=month). \
                annotate(date=TruncDay('created_date')). \
                values('date').annotate(count=Sum('total'))
            resp = []
            for i in stat.iterator():
                # print(i)
                resp.append({
                    str(i['date']) : i['count']
                })
            print(resp)
            return JsonResponse({'static_list':resp})
        if range == 'year':
            year = timezone.now().year
            stat = models.Bill.objects. \
                filter(created_date__year=year). \
                annotate(month=TruncMonth('created_date')). \
                values('month').annotate(count=Sum('total'))
            resp = []
            for i in stat.iterator():
                print(i)
                resp.append({
                    str(i['month'].month): i['count']
                })
            return JsonResponse({'static_list':resp})
    return render(request, 'admin/bill/statistics.html')

@user_passes_test(is_admin)
def customerProfile(request):
    id = request.GET['id']
    customer = models.User.objects.get(pk = id)
    context = {
        'customer':customer
    }
    return render(request, 'admin/customer/profile.html',context)

@user_passes_test(is_admin)
def customerOrdersList(request):
    id = request.GET['id']
    bills = models.Bill.objects.filter(user_id=id)
    context = {
        'bill_list':bills
    }
    return render(request, 'admin/customer/orders.html',context)

@user_passes_test(is_admin)
def customers(request):
    customer_list = models.User.objects.filter(role='mem')
    context = {
        'customer_list':customer_list
    }
    return render(request, 'admin/customer/index.html',context)