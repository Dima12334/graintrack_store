from graintrack_store.api.v1.products.product_categories.serializers import (
    ProductCategoryGetSerializer,
)
from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.core.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES
from graintrack_store.products.constants import ProductConstants
from graintrack_store.products.models import Product
from rest_framework import serializers as drf_serializers


class ProductGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    created_at = drf_serializers.DateTimeField(read_only=True)
    is_deleted = drf_serializers.BooleanField(read_only=True)
    name = drf_serializers.CharField(read_only=True)
    category = ProductCategoryGetSerializer(read_only=True)
    price = drf_serializers.DecimalField(
        read_only=True, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES
    )
    description = drf_serializers.CharField(read_only=True)
    available_quantity = drf_serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "uuid",
            "created_at",
            "is_deleted",
            "name",
            "category",
            "price",
            "description",
            "available_quantity",
        )


class ProductCreateSerializer(BaseProjectModelSerializer):
    name = drf_serializers.CharField(
        required=True, max_length=ProductConstants.NAME_MAX_LENGTH
    )
    category_uuid = drf_serializers.UUIDField(required=True)
    price = drf_serializers.DecimalField(
        required=True, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES
    )
    description = drf_serializers.CharField(
        required=False,
        default="",
        allow_blank=True,
        max_length=ProductConstants.DESCRIPTION_MAX_LENGTH,
    )

    class Meta:
        model = Product
        fields = ("name", "category_uuid", "price", "description")


class ProductUpdateSerializer(BaseProjectModelSerializer):
    is_deleted = drf_serializers.BooleanField(required=False)
    name = drf_serializers.CharField(
        required=False, max_length=ProductConstants.NAME_MAX_LENGTH
    )
    category_uuid = drf_serializers.UUIDField(required=False)
    price = drf_serializers.DecimalField(
        required=False, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES
    )
    description = drf_serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=ProductConstants.DESCRIPTION_MAX_LENGTH,
    )

    class Meta:
        model = Product
        fields = ("is_deleted", "name", "category_uuid", "price", "description")


class CategoryNameAndProductsCountSerializer(drf_serializers.Serializer):
    category_name = drf_serializers.CharField(read_only=True)
    products_count = drf_serializers.IntegerField(read_only=True)


class SoldProductsReportSerializer(drf_serializers.Serializer):
    sold_products_with_discount_count = drf_serializers.IntegerField(read_only=True)
    all_sold_products_count = drf_serializers.IntegerField(read_only=True)
    sold_products_by_categories = drf_serializers.ListField(
        child=CategoryNameAndProductsCountSerializer()
    )
