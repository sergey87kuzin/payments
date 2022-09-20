import os
import logging

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from dotenv import load_dotenv

from .models import Coupon, Item, OrderCounts, Order, Tax
from .forms import (
    CouponForm, ModifForm, OrderForm, ItemForm, TaxForm
)

load_dotenv()
logger = logging.getLogger('django')
stripe.api_key = os.getenv('API_KEY')


def get_item(request, id):
    logger.warning('добрался до страницы товара')
    form = ModifForm(request.POST or None)
    item = get_object_or_404(Item, id=id)
    pushable_key = os.getenv('PUBLISHABLE_KEY')
    logger.warning(f'key = { pushable_key }')
    context = {'item': item, 'key': pushable_key, 'form': form}
    return render(request, 'item.html', context=context)


@csrf_exempt
def buy_item(request, id):
    if request.method == 'GET':
        item = get_object_or_404(Item, id=id)
        # tax = Tax.objects.first()
        tax, coupons = start_buying()
        if tax:
            items = {
                # 'price_data': {
                #     'currency': item.currency,
                #     'unit_amount': item.price,
                #     'product_data': {
                #         'name': item.name,
                #         'description': item.description,
                #     },
                # },
                'price': item.price_id,
                'quantity': 1,
                'tax_rates': [tax.tax_id]
            }
        else:
            items = {
                'price': item.price_id,
                'quantity': 1
            }
        # coupon = Coupon.objects.first()
        # coupons = {}
        # if coupon:
        #     coupons = {'coupon': coupon.coupon_id}
        # stripe.api_key = os.getenv('API_KEY')
        logger.warning('добрался до создания платежа')
        try:
            session = stripe.checkout.Session.create(
                line_items=[items],
                mode='payment',
                discounts=[coupons],
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/bad_request/',
            )
            return JsonResponse({'sessionId': session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def create_coupon(request):
    form = CouponForm(request.POST or None)
    pub_key = os.getenv('PUBLISHABLE_KEY')
    if 'create_button' in request.POST:
        if form.is_valid():
            name = form.cleaned_data['name']
            percent_off = form.cleaned_data['percent_off']
            try:
                coupon = stripe.Coupon.create(
                    percent_off=percent_off, name=name, duration="once"
                )
                Coupon.objects.create(
                    name=coupon['name'],
                    coupon_id=coupon['id']
                )
            except Exception as e:
                logger.error(str(e))
    context = {'form': form, 'key': pub_key, 'title': 'создание скидки'}
    return render(request, 'create_item.html', context)


def create_tax(request):
    form = TaxForm(request.POST or None)
    pub_key = os.getenv('PUBLISHABLE_KEY')
    if 'create_button' in request.POST:
        if form.is_valid():
            name = form.cleaned_data['name']
            percentage = form.cleaned_data['percentage']
            try:
                tax = stripe.TaxRate.create(
                    percentage=percentage, display_name=name,
                    inclusive=False
                )
                Tax.objects.create(
                    name=tax['display_name'],
                    tax_id=tax['id']
                )
            except Exception as e:
                logger.error(str(e))
    context = {'form': form, 'key': pub_key, 'title': 'создание налога'}
    return render(request, 'create_item.html', context)


def create_order(request):
    order = Order.objects.first()
    if not order:
        order = Order.objects.create()
    form = OrderForm(request.POST or None)
    pub_key = os.getenv('PUBLISHABLE_KEY')
    if 'add_item' in request.POST:
        if form.is_valid():
            items = Item.objects.filter(id=form.cleaned_data['item'])
            if items:
                OrderCounts.objects.create(
                    order=order,
                    item=items[0],
                    quantity=form.cleaned_data['quantity']
                )
    return render(request, 'order.html', {'form': form, 'key': pub_key})


@csrf_exempt
def buy_order(request):
    ''' формирует сессию с учетом всех товаров в заказе, налогов и скидок '''
    if request.method == 'GET':
        order = Order.objects.first()
        counts = OrderCounts.objects.filter(order=order)
        # tax = Tax.objects.first()
        tax, coupons = start_buying()
        if tax:
            items = [{
                # 'price_data': {
                #     'currency': count.item.currency,
                #     'unit_amount': count.item.price,
                #     'product_data': {
                #         'name': count.item.name,
                #         'description': count.item.description,
                #     },
                # },
                'price': count.item.price_id,
                'quantity': count.quantity,
                'tax_rates': [tax.tax_id]
            } for count in counts]
        else:
            items = [{
                'price': count.item.price_id,
                'quantity': count.quantity,
            } for count in counts]
        # coupon = Coupon.objects.first()
        # coupons = {}
        # if coupon:
        #     coupons = {'coupon': coupon.coupon_id}
        # stripe.api_key = os.getenv('API_KEY')
        order_list = [
            f'{count.item.name} - {count.quantity}' for count in counts
        ]
        logger.warning('добрался до обработки заказа' +
                       ', '.join(order_list))
        try:
            session = stripe.checkout.Session.create(
                line_items=items,
                mode='payment',
                discounts=[coupons],
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/bad_request/',
            )
            return JsonResponse({'sessionId': session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def create_price(request):
    form = ItemForm(request.POST or None)
    pub_key = os.getenv('PUBLISHABLE_KEY')
    if 'create_button' in request.POST:
        logger.warning('проверка формы')
        if form.is_valid():
            logger.warning('создаю объект цены')
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            try:
                item = stripe.Product.create(
                    name=name, description=description
                )
                amount = stripe.Price.create(
                    unit_amount=int(price) * 100,
                    currency='usd',
                    product=item['id'],
                    currency_options={
                        'eur': {
                            'unit_amount': int(price) * 101
                        },
                        'jpy': {
                            'unit_amount': int(price) * 7500
                        }
                    }
                )
                new_item = Item.objects.create(
                    name=item['name'],
                    description=item['description'],
                    price=int(price),
                    currency=amount['currency'],
                    price_id=amount['id'])
                return redirect('items', id=new_item.id)
            except Exception as e:
                logger.error(str(e))
    return render(request, 'create_item.html',
                  {'form': form, 'key': pub_key, 'title': 'Товар'})


def success(request):
    OrderCounts.objects.all().delete()
    return render(request, 'success.html')


def bad_request(request):
    OrderCounts.objects.all().delete()
    return render(request, 'bad_request.html')


def start_buying():
    tax = Tax.objects.first()
    coupon = Coupon.objects.first()
    coupons = {}
    if coupon:
        coupons = {'coupon': coupon.coupon_id}
    stripe.api_key = os.getenv('API_KEY')
    return tax, coupons
