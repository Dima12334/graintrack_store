from django.db import models

from graintrack_store.core.constants import (
    DECIMAL_MAX_DIGITS,
    DECIMAL_PLACES,
    DECIMAL_PLACES_FOR_PERCENT,
    DECIMAL_MAX_DIGITS_FOR_PERCENT,
)
from graintrack_store.core.models import BaseModel
from graintrack_store.products.constants import (
    ProductConstants,
    ProductCategoryConstants,
)


class ProductCategory(BaseModel):
    name = models.CharField(max_length=ProductCategoryConstants.NAME_MAX_LENGTH)
    description = models.CharField(
        max_length=ProductCategoryConstants.DESCRIPTION_MAX_LENGTH, default=""
    )
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        default=None,
        related_name="child_categories",
    )

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"
        db_table = "product_categories"


class Product(BaseModel):
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=ProductConstants.NAME_MAX_LENGTH)
    category = models.ForeignKey(
        ProductCategory, null=False, related_name="products", on_delete=models.PROTECT
    )
    price = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES
    )
    description = models.CharField(
        max_length=ProductConstants.DESCRIPTION_MAX_LENGTH, default=""
    )
    available_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"


class ProductIncome(BaseModel):
    product = models.ForeignKey(
        Product, null=False, related_name="product_incomes", on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Product income"
        verbose_name_plural = "Product incomes"
        db_table = "product_incomes"


class ProductDiscount(BaseModel):
    product = models.OneToOneField(
        Product, null=False, related_name="product_discount", on_delete=models.CASCADE
    )
    discount_started_at = models.DateTimeField()
    discount_ended_at = models.DateTimeField()
    discount_percentage = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product discount"
        verbose_name_plural = "Product discounts"
        db_table = "product_discounts"
