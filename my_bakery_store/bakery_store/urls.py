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
    path('add_comment', views.add_comment, name='add_comment'),
    path('admin/product', views.ProductsIndex, name='view_product'),
    path('admin/product/list', views.GetListProducts, name='list_products'),
    path('admin/product/edit', views.edit_product, name='edit_product'),
    path('admin/product/delete', views.deleteProduct, name = 'delete_product'),
    # path('admin/product/delete', views.delete, name='delete_product')
    path('change_quantity_on_cart', views.change_quantity_on_cart, name='change_quantity_on_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('order_complete', views.order_complete, name ='order_complete'),
    path('admin/bill/index',views.billIndex, name = 'billIndex'),
    path('admin/bill/detail', views.billDetail, name = 'billDetail'),
    path('admin/product/statistics', views.statisticsProductForm, name="statisticsProduct"),
    path('VA/profile', views.profile, name='profile'),
    path('admin/bill/approve', views.approveBill, name = 'approveBill'),
    path('admin/event', views.eventIndex, name= 'eventIndex'),
    path('admin/event/create',views.createEvent, name='createEvent'),
    path('admin/event/edit', views.editEventForm, name='editEvent'),
    path('admin/event/change', views.eventChange, name='eventChange'),
    path('VA/orders', views.customerOrders, name='customerOrders'),
    path('VA/order/detail', views.customerOrderDetail, name='customerOrderDetail')

]