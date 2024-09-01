from graintrack_store.api.v1.products.product_categories.serializers import (
    ProductCategoryGetSerializer,
)
from graintrack_store.api.v1.products.products.serializers import ProductGetSerializer
from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.core.constants import (
    DECIMAL_MAX_DIGITS,
    DECIMAL_PLACES,
    DECIMAL_MAX_DIGITS_FOR_PERCENT,
    DECIMAL_PLACES_FOR_PERCENT,
)
from graintrack_store.products.constants import ProductConstants
from graintrack_store.products.models import ProductDiscount
from rest_framework import serializers as drf_serializers


class ProductDiscountGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    created_at = drf_serializers.DateTimeField(read_only=True)
    product = ProductGetSerializer(read_only=True)
    discount_started_at = drf_serializers.DateTimeField(read_only=True)
    discount_ended_at = drf_serializers.DateTimeField(read_only=True)
    discount_percentage = drf_serializers.DecimalField(
        read_only=True,
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
    )
    is_active = drf_serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductDiscount
        fields = (
            "uuid",
            "created_at",
            "product",
            "discount_started_at",
            "discount_ended_at",
            "discount_percentage",
            "is_active",
        )


class ProductDiscountCreateSerializer(BaseProjectModelSerializer):
    product_uuid = drf_serializers.UUIDField(required=True)
    discount_started_at = drf_serializers.DateTimeField(required=True)
    discount_ended_at = drf_serializers.DateTimeField(required=True)
    discount_percentage = drf_serializers.DecimalField(
        required=True,
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
    )

    class Meta:
        model = ProductDiscount
        fields = (
            "product_uuid",
            "discount_started_at",
            "discount_ended_at",
            "discount_percentage",
        )


class ProductDiscountUpdateSerializer(BaseProjectModelSerializer):
    is_active = drf_serializers.BooleanField(required=False)
    discount_started_at = drf_serializers.DateTimeField(required=False)
    discount_ended_at = drf_serializers.DateTimeField(required=False)
    discount_percentage = drf_serializers.DecimalField(
        required=False,
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
    )

    class Meta:
        model = ProductDiscount
        fields = (
            "is_active",
            "discount_started_at",
            "discount_ended_at",
            "discount_percentage",
        )
