from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.get_item, name='items'),
    path('buy/<int:id>/', views.buy_item, name='buy'),
    path('create_price/', views.create_price, name='create_price'),
    path('create_coupon/', views.create_coupon, name='create_coupon'),
    path('create_tax/', views.create_tax, name='create_tax'),
    path('buy_order/', views.buy_order, name='buy_order'),
    path('order/', views.create_order, name='create_order'),
    path('success/', views.success, name='success'),
    path('bad_request/', views.bad_request, name='bad_request')
]
