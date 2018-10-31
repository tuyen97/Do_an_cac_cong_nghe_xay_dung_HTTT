# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=191)
    birth_day = models.DateTimeField
    address = models.CharField
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
    USERNAME_FIELD = 'user_name'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    available_quantity = models.IntegerField(max_length=9)
    descript = models.CharField
    price = models.IntegerField(max_length=11)
    category = models.CharField(max_length=30)
    image = models.ImageField(upload_to="images")
    is_deleted = models.BooleanField(default=True)

class Lot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp_date = models.DateField
    mfg_date = models.DateField
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
