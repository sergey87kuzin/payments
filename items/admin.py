from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Coupon, Item, Order, OrderCounts, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_items',)


class OrderCountsAdmin(admin.ModelAdmin):
    list_display = ('item', 'order', 'quantity')


class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'coupon_id')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_id')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderCounts, OrderCountsAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.unregister(Group)
