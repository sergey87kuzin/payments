from django.db import models
from django.core.exceptions import ValidationError


class Item(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=30
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255
    )
    price = models.IntegerField(
        verbose_name='Цена',
    )
    currency = models.CharField(
        verbose_name='валюта', max_length=3, default='usd'
    )
    price_id = models.CharField(verbose_name='ID цены', max_length=40)
    order = models.ManyToManyField(
        'Order', related_name='items', through='OrderCounts')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def clean(self):
        if self.price < 0:
            raise ValidationError('Цена почему отрицательная?')

    def __str__(self):
        return f'Прекрасный товар {self.name}'


class Order(models.Model):
    item = models.ManyToManyField(
        'Item', related_name='orders', through='OrderCounts'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_items(self):
        results = []
        items = list(Item.objects.filter(
            order__id=self.id).values_list('name')
        )
        for item in items:
            results.append(item[0])
        return ', '.join(results)


class Coupon(models.Model):
    name = models.CharField(verbose_name='имя купона', max_length=30)
    coupon_id = models.CharField(verbose_name='ID купона', max_length=40)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class Tax(models.Model):
    name = models.CharField(verbose_name='имя купона', max_length=30)
    tax_id = models.CharField(verbose_name='ID налога', max_length=40)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class OrderCounts(models.Model):
    item = models.ForeignKey(
        'Item', on_delete=models.CASCADE, verbose_name='товар'
    )
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, verbose_name='заказ'
    )
    quantity = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        ordering = ('item',)
        verbose_name = 'Количество'
        verbose_name_plural = 'количества'
