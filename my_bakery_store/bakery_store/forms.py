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
    user_name = forms.CharField(label='User Name',widget=forms.TextInput(attrs=add_attrs('Enter user name')))
    full_name = forms.CharField(label='Full Name',widget=forms.TextInput(attrs=add_attrs('Enter name')))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs=add_attrs('Enter email')))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=add_attrs('Enter password')))
    birth_day = forms.DateTimeField(label='Birth day',widget=forms.DateTimeInput(attrs={'class':'form-control datepicker','id':'datepicker'}))
    address = forms.CharField(label='address',widget=forms.TextInput(attrs=add_attrs('Enter address')))
    gender = forms.ChoiceField(label='Gender', choices=models.User.SEX_CHOICES, widget=forms.Select({'class': 'form-control'}))

    class Meta:
        model = models.User
        fields = ['user_name','full_name','email','password','birth_day','address','gender']

class loginForm(forms.Form):
    user_name = forms.CharField(label='User Name',widget=forms.TextInput(attrs=add_attrs('Enter user name')))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=add_attrs('Enter password')))

