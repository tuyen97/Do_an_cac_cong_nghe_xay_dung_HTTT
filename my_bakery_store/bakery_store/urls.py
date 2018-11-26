from . import views
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path("",views.index,name='index'),
    path('register', views.register, name='register'),
    path('login/', views.loginView, name='loginView'),
    path('logout/', views.Logout,name = 'logout'),
    path('admin/', views.admin_index, name = 'admin_index'),
    path('admin/add_product', views.add_product, name='add_product'),
    path('product_detail',views.product_detail, name='product_detail'),
    path('add_to_cart',views.add_to_cart, name='add_to_cart'),
    path('view_cart', views.view_cart,name='view_cart'),
    path('delete_product_on_cart', views.delete_product_on_cart, name='delete_product_on_cart'),
    path('change_quantity_on_cart', views.change_quantity_on_cart, name='change_quantity_on_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('order_complete', views.order_complete, name ='order_complete')

]