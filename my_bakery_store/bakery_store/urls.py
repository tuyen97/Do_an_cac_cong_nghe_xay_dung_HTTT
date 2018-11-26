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
    path('view_cart', views.view_cart,name='view_cart'),
    path('delete_product_on_cart', views.delete_product_on_cart, name='delete_product_on_cart'),
    path('admin/product', views.ProductsIndex, name='view_product'),
    path('admin/product/list', views.GetListProducts, name='list_products'),
    path('admin/product/edit', views.edit_product, name='edit_product'),
    # path('admin/product/delete', views.delete, name='delete_product')

]