from django import forms
from .models import Coupon, Item, Tax


def get_items():
    return ((item.id, item.name) for item in OrderForm.item_list)


def get_coupons():
    return ((coupon.id, coupon.name) for coupon in ModifForm.coupon_list)


def get_tax():
    return ((tax.id, tax.name) for tax in ModifForm.tax_list)


class OrderForm(forms.Form):
    item_list = Item.objects.all()
    item = forms.ChoiceField(
        choices=get_items, required=False, label='товар'
    )
    quantity = forms.IntegerField(
        max_value=15, min_value=1, required=False, label='количество'
    )


class ItemForm(forms.Form):
    name = forms.CharField(max_length=30, label='наименование')
    description = forms.CharField(max_length=255, label='описание')
    price = forms.DecimalField(
        min_value=0, max_digits=10, decimal_places=2, label='цена'
    )


class CouponForm(forms.Form):
    name = forms.CharField(max_length=30, label='имя купона')
    percent_off = forms.DecimalField(
        max_value=100, min_value=0, decimal_places=2, label='размер скидки'
    )


class TaxForm(forms.Form):
    name = forms.CharField(max_length=30, label='имя налога')
    percentage = forms.DecimalField(
        max_value=100, min_value=0, decimal_places=2, label='размер налога'
    )


class ModifForm(forms.Form):
    coupon_list = Coupon.objects.all()
    tax_list = Tax.objects.all()
    coupon = forms.ChoiceField(
        choices=get_coupons, required=False, label='скидка'
    )
    tax = forms.ChoiceField(
        choices=get_tax, required=False, label='налог'
    )
