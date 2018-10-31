from django import forms
from . import models

def add_attrs(placeholder='', display=True):

    attrs =  {
        'class': 'form-control',
        'placeholder': placeholder
    }
    if not display:
        attrs['style'] = 'display: none;'
    return attrs

class registerForm(forms.ModelForm):
    username = forms.CharField(label='User Name',widget=forms.TextInput(attrs=add_attrs('Enter user name')))
    full_name = forms.CharField(label='Full Name',widget=forms.TextInput(attrs=add_attrs('Enter name')))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs=add_attrs('Enter email')))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=add_attrs('Enter password')))
    birth_day = forms.DateTimeField(label='Birth day',widget=forms.DateTimeInput(attrs={'class':'form-control datepicker','id':'datepicker'}))
    address = forms.CharField(label='address',widget=forms.TextInput(attrs=add_attrs('Enter address')))
    gender = forms.ChoiceField(label='Gender', choices=models.User.SEX_CHOICES, widget=forms.Select({'class': 'form-control'}))
    avt = forms.ImageField(label='Chọn ảnh', widget=forms.FileInput(add_attrs('')))
    class Meta:
        model = models.User
        fields = ['username','full_name','email','password','birth_day','address','gender','avt']

class loginForm(forms.Form):
    user_name = forms.CharField(label='User Name',widget=forms.TextInput(attrs=add_attrs('Enter user name')))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=add_attrs('Enter password')))

class productForm(forms.ModelForm):
    name = forms.CharField(label='Tên sản phẩm', widget=forms.TextInput(attrs=add_attrs()))
    available_quantity = forms.IntegerField(label='Số lượng',widget=forms.NumberInput(add_attrs('Nhập số lượng')))
    descript = forms.CharField(label='Mô tả', widget=forms.TextInput(add_attrs('Mô tả')))
    price = forms.IntegerField(label='Giá', widget=forms.NumberInput(add_attrs('Nhập giá')))
    category = forms.CharField(label='Loại', widget=forms.TextInput(add_attrs('Nhập loại')))
    image = forms.ImageField(label='Chọn ảnh',  widget=forms.FileInput(add_attrs('')))

    class Meta:
        model = models.Product
        fields = ['name','available_quantity','descript','price','category','image']
