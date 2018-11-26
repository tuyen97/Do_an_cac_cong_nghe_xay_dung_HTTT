# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100,unique=True, default="")
    full_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=191)
    birth_day = models.DateTimeField(null=False, default= "")
    address = models.CharField(max_length=1000,default="")
    ADMIN = 'ad'
    MEMBER = 'mem'
    POSITION_CHOICES = (
        (ADMIN, 'ad'),
        (MEMBER, 'mem')
    )
    MALE = 'm'
    FEMALE = 'f'
    SEX_CHOICES=(
        (MALE,'nam'),
        (FEMALE,'nữ')
    )
    gender = models.CharField(max_length=2,choices=SEX_CHOICES)
    role = models.CharField(max_length=2,choices=POSITION_CHOICES,default=MEMBER)
    avt = models.ImageField(upload_to="images/user",null=True)
    USERNAME_FIELD = 'user_name'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    available_quantity = models.IntegerField()
    descript = models.CharField(max_length=10000000, default="")
    price = models.IntegerField()
    category = models.CharField(max_length=30)
    image = models.ImageField(upload_to="images")
    is_deleted = models.BooleanField(default=True)

class Lot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp_date = models.DateField
    mfg_date = models.DateField
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

class Bill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('User',on_delete=models.CASCADE, null=True)
    created_date = models.DateField(null=False,default='')
    total = models.IntegerField()
    SUCCESS = 'succ'
    FAIL ='fail'
    PROCESSING = 'proc'
    STATUS =(
        (SUCCESS,'Thành công'),
        (FAIL,'Thất bại'),
        (PROCESSING,'Đang xử lí')
    )
    PAYPAL = 'pp'
    TIEN_MAT = 'tm'
    PAY_METHOD_CHOICES =(
        (PAYPAL,'paypal'),
        (TIEN_MAT,'tiền mặt')
    )
    status = models.CharField(choices=STATUS, default=PROCESSING, max_length=4)
    payment = models.CharField(choices=PAY_METHOD_CHOICES, max_length=4)
    receiver_name = models.CharField(max_length=100, null=False)
    receiver_address = models.CharField(max_length=100, null=False)
    receiver_phone = models.IntegerField(null=False)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateField(null=False,default='')
    finish_time = models.DateField(null=False,default='')
    sale_off = models.IntegerField(null=False,max_length=2)

class BillDetail(models.Model):
    product_id = models.ForeignKey('Product',on_delete=models.CASCADE)
    event_id = models.ForeignKey('Event',on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=False)
    total = models.IntegerField(null=False)
    bill_id = models.ForeignKey('Bill', on_delete=models.CASCADE)
