from decimal import Decimal

from django.db import models

from graintrack_store.core.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES
from graintrack_store.core.models import BaseModel
from graintrack_store.products.models import Product
from graintrack_store.orders.constants import OrderConstants
from graintrack_store.users.models import User


class Order(BaseModel):
    creator = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    status = models.CharField(max_length=OrderConstants.STATUS_MAX_LENGTH, choices=OrderConstants.STATUS_CHOICE)
    order_code = models.CharField(max_length=OrderConstants.ORDER_CODE_MAX_LENGTH)
    comment = models.CharField(max_length=OrderConstants.COMMENT_MAX_LENGTH, default="")
    total_sum = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "orders"


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, related_name="order_products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_products", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    discount = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=Decimal(0))

    class Meta:
        verbose_name = "Order product"
        verbose_name_plural = "Order products"
        db_table = "order_products"
