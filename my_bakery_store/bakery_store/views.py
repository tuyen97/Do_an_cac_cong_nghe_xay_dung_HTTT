# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from . import forms
from django.contrib.auth import logout, login
from .security.MyBackend import MyBackend

# Create your views here.

def index(request):
    return render(request,'bakery_store/shop.html')

def register(request):
    form = forms.registerForm()
    if request.method == "POST":
        f = forms.registerForm(request.POST)
        if f.is_valid():
            print(f.cleaned_data['user_name'])
            print(f.cleaned_data['password'])
            f.save()
            return HttpResponse('success')
        else:
            return render(request,"bakery_store/register.html",{'form':f})
    else:
        return render(request,"bakery_store/register.html",{'form':form})

def loginView(request):
    f = forms.loginForm()
    if request.method == "POST":
        f = forms.loginForm(request.POST)
        if(f.is_valid()):
            user_name = f.cleaned_data['user_name']
            password = f.cleaned_data['password']
            user = MyBackend.authenticate(request, user_name=user_name,password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                return render(request,"bakery_store/shop.html")
            else:
                return HttpResponse("Login fail")
        else:
            return render(request,'bakery_store/login.html',{'form':f})
    else:
        return render(request,'bakery_store/login.html',{'form':f})

