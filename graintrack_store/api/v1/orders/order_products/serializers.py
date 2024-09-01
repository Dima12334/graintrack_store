from graintrack_store.api.v1.orders.orders.serializers import OrderGetSerializer
from graintrack_store.api.v1.products.products.serializers import ProductGetSerializer
from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.core.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES
from graintrack_store.orders.models import OrderProduct
from rest_framework import serializers as drf_serializers


class OrderProductGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    created_at = drf_serializers.DateTimeField(read_only=True)
    order = OrderGetSerializer(read_only=True)
    product = ProductGetSerializer(read_only=True)
    quantity = drf_serializers.IntegerField(read_only=True)
    price = drf_serializers.DecimalField(
        read_only=True, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES
    )
    price_with_discount = drf_serializers.DecimalField(
        read_only=True,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )
    discount = drf_serializers.DecimalField(
        read_only=True,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )

    class Meta:
        model = OrderProduct
        fields = (
            "uuid",
            "created_at",
            "order",
            "product",
            "quantity",
            "price",
            "price_with_discount",
            "discount",
        )


class OrderProductCreateSerializer(BaseProjectModelSerializer):
    order_uuid = drf_serializers.UUIDField(required=True)
    product_uuid = drf_serializers.UUIDField(required=True)
    quantity = drf_serializers.IntegerField(required=True)

    class Meta:
        model = OrderProduct
        fields = ("order_uuid", "product_uuid", "quantity")


class OrderProductUpdateSerializer(BaseProjectModelSerializer):
    quantity = drf_serializers.IntegerField(required=False)

    class Meta:
        model = OrderProduct
        fields = ("quantity",)
