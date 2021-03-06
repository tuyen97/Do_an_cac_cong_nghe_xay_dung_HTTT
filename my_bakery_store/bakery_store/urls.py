from . import views
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path("",views.index,name='index'),
    path('search',views.search, name = 'search'),
    path('register', views.register, name='register'),
    path('login', views.loginView, name='loginView'),
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
    path('admin/bill/statstics', views.statisticsRevenueForm, name='statisticRevenue'),
    path('admin/product/statistics', views.statisticsProduct, name="statisticsProduct"),
    path('profile', views.profile, name='profile'),
    path('admin/bill/approve', views.approveBill, name = 'approveBill'),
    path('admin/event', views.eventIndex, name= 'eventIndex'),
    path('admin/event/create',views.createEvent, name='createEvent'),
    path('admin/event/edit', views.editEventForm, name='editEvent'),
    path('admin/event/change', views.eventChange, name='eventChange'),
    #
    # path('VA/orders', views.customerOrders, name='customerOrders'),
    #
    # path('VA/order/detail', views.customerOrderDetail, name='customerOrderDetail'),
    # path('VA/admin/bill/statistics', views.statisticsRevenueForm, name="statisticsRevenueForm"),
    #
    #
    #
    # path('VA/order/detail', views.customerOrderDetail, name='customerOrderDetail')


    path('orders', views.customerOrders, name='customerOrders'),
    path('order/detail', views.customerOrderDetail, name='customerOrderDetail'),
    #
    path('admin/customer', views.customers, name='customers'),
    path('admin/customer/ordersList', views.customerOrdersList, name='customerOrderList'),
    path('admin/customer/profile', views.customerProfile, name='customerProfile')

]