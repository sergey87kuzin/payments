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

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def clean(self):
        if self.price < 0:
            raise ValidationError('Цена почему отрицательная?')

    def __str__(self):
        return f'Прекрасный товар {self.name}'
