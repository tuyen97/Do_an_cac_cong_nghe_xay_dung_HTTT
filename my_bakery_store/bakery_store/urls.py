from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name='index'),
    path('register', views.register, name='register'),
    path('login/', views.loginView, name='loginView'),
    path('logout/', views.Logout,name = 'logout'),
    path('admin/', views.admin_index, name = 'admin_index'),
    path('admin/add_product', views.add_product, name='add_product'),
    path('product_detail',views.product_detail, name='product_detail'),
    path('add_to_cart',views.add_to_cart, name='add_to_cart'),
    path('view_cart', views.view_cart,name='view_cart')

]