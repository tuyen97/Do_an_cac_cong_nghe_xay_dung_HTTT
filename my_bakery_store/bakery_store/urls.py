from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name='index'),
    path('register', views.register, name='register'),
    path('Login', views.loginView, name='loginView'),
    path('logout', views.Logout,name = 'logout'),
    path('admin/add_product', views.add_product, name='add_product'),
    path('child1', views.child1, name='child1'),
    path('product_detail', views.productDetail, name='product_detail')
]