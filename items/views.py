import json
import os
import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from dotenv import load_dotenv

from .models import Item

load_dotenv()
logger = logging.getLogger('django')
stripe.api_key = os.getenv('API_KEY')


def get_item(request, id):
    logger.warning('добрался до страницы товара')
    item = get_object_or_404(Item, id=id)
    pushable_key = os.getenv('PUBLISHABLE_KEY')
    logger.warning(f'key = { pushable_key }')
    context = {'item': item, 'key': pushable_key}
    return render(request, 'item.html', context=context)


@csrf_exempt
def buy_item(request, id):
    if request.method == 'GET':
        item = get_object_or_404(Item, id=id)
        stripe.api_key = os.getenv('API_KEY')
        logger.warning('добрался до создания платежа')
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': item.price,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                },
                'quantity': 1
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/failure',
        )

        # session, err = session.New(params)
        # 303 redirect to session.url
        return JsonResponse({'sessionId': session['id']})


def exit(request):
    return render(request, 'exit.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': os.getenv('PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400
