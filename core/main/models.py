from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):

    name = models.CharField('Product name', max_length=30)
    price = models.IntegerField('Product price')
    img = models.ImageField('Product image')
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-id']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([item.get_total for item in orderproducts])
        return total

    @property
    def get_itemtotal(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([item.quantity for item in orderproducts])
        return total

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    @property
    def get_cart_all_total(self):
        total = self.get_cart_total + 2
        return total


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'orderproduct'
        verbose_name_plural = 'orederproducts'
        ordering = ['user_id']