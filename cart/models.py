from django.db import models
from customer.models import Customer
from product.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="cart",
    )

    @property
    def totalPrice(self):
        total = 0
        for item in self.items.all():
            total += item.totalPrice
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="items",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )
    quantity = models.IntegerField()

    @property
    def totalPrice(self):
        price = self.product.price
        total = price * self.quantity
        return total
