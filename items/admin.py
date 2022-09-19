from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Item, ItemAdmin)
admin.site.unregister(Group)
