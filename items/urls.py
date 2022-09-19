from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.get_item, name='items'),
    path('buy/<int:id>/', views.buy_item, name='buy'),
    path('exit/', views.exit, name='exit'),
    path('config/', views.stripe_config)
]
