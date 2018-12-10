from django import forms
from . import models

class DateTypeInput(forms.DateInput):
    input_type = 'date'

def add_attrs(placeholder='', display=True):

    attrs =  {
        'class': 'form-control',
        'placeholder': placeholder
    }
    if not display:
        attrs['style'] = 'display: none;'
    return attrs

class registerForm(forms.ModelForm):
    user_name = forms.CharField(label='User Name',widget=forms.TextInput(attrs=add_attrs('Enter user name')))
    full_name = forms.CharField(label='Full Name',widget=forms.TextInput(attrs=add_attrs('Enter name')))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs=add_attrs('Enter email')))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=add_attrs('Enter password')))
    birth_day = forms.DateTimeField(label='Birth day',widget=DateTypeInput(attrs={'class':'form-control datepicker','id':'datepicker'}))
    address = forms.CharField(label='address',widget=forms.TextInput(attrs=add_attrs('Enter address')))
    gender = forms.ChoiceField(label='Gender', choices=models.User.SEX_CHOICES, widget=forms.Select({'class': 'form-control'}))
    avt = forms.ImageField(label='Chọn ảnh', widget=forms.FileInput(add_attrs('')))
    class Meta:
        model = models.User
        fields = ['user_name','full_name','email','password','birth_day','address','gender','avt']

class loginForm(forms.Form):
    user_name = forms.CharField(label='User Name',widget=forms.TextInput(attrs=add_attrs('Enter user name')))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=add_attrs('Enter password')))

class productForm(forms.ModelForm):
    name = forms.CharField(label='Tên sản phẩm', widget=forms.TextInput(attrs=add_attrs()))
    available_quantity = forms.IntegerField(label='Số lượng',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Nhập số lượng','min':1}))
    descript = forms.CharField(label='Mô tả', widget=forms.Textarea(add_attrs('Mô tả')))
    price = forms.IntegerField(label='Giá', widget=forms.NumberInput(add_attrs('Nhập giá')))
    category = forms.CharField(label='Loại', widget=forms.TextInput(add_attrs('Nhập loại')))
    image = forms.ImageField(label='Chọn ảnh',  widget=forms.FileInput(add_attrs('')))

    class Meta:
        model = models.Product
        fields = ['name','available_quantity','descript','price','category','image']

class checkoutForm(forms.Form):
    PAYPAL = 'pp'
    TIEN_MAT = 'tm'
    PAY_METHOD_CHOICES =(
        (PAYPAL,'paypal'),
        (TIEN_MAT,'tiền mặt')
    )
    hoten = forms.CharField(label="Họ tên", widget=forms.TextInput(attrs=add_attrs('Họ tên')))
    diachi = forms.CharField(label='Địa chỉ',widget=forms.TextInput(attrs=add_attrs('Địa chỉ')))
    sdt = forms.IntegerField(label='Số điện thoại',widget=forms.TextInput(attrs=add_attrs('Số điện thoại')))
    # pay_method = forms.ChoiceField(label='Phương thức thanh toán',choices=PAY_METHOD_CHOICES,widget=forms.Select({'class':'form-control'}))

class editProduct(forms.ModelForm):
    name = forms.CharField(label='Tên sản phẩm', widget=forms.TextInput(attrs=add_attrs()))
    available_quantity = forms.IntegerField(label='Số lượng',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Nhập số lượng','min':1}))
    descript = forms.CharField(label='Mô tả', widget=forms.Textarea(add_attrs('Mô tả')))
    price = forms.IntegerField(label='Giá', widget=forms.NumberInput(add_attrs('Nhập giá')))
    category = forms.CharField(label='Loại', widget=forms.TextInput(add_attrs('Nhập loại')))
    image = forms.ImageField(required=False,label='Chọn ảnh', widget=forms.FileInput(add_attrs('')))
    class Meta:
        model = models.Product
        fields = ['name','available_quantity','descript','price','category','image']

class addComment(forms.ModelForm):
    image = forms.ImageField(required=False, label='Chọn ảnh', widget=forms.FileInput(add_attrs('')))
    content = forms.CharField(label='Nội dung bình luận', widget=forms.Textarea(add_attrs('Bình luận')))
    class Meta:
        model = models.Comment
        fields = ['content','image']


class approveBill(forms.Form):
    SUCCESS = 'succ'
    FAIL ='fail'
    STATUS =(
        (SUCCESS,'Thành công'),
        (FAIL,'Thất bại'),
    )
    status = forms.ChoiceField(label='Duyệt trạng thái',choices=STATUS,widget=forms.Select({'class':'form-control'}))