from graintrack_store.api.v1.auth.serializers import UserGetSerializer
from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.core.constants import (
    DECIMAL_MAX_DIGITS,
    DECIMAL_PLACES,
    DECIMAL_MAX_DIGITS_FOR_PERCENT,
    DECIMAL_PLACES_FOR_PERCENT,
)
from graintrack_store.orders.constants import OrderConstants
from graintrack_store.orders.models import Order
from rest_framework import serializers as drf_serializers


class OrderGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    created_at = drf_serializers.DateTimeField(read_only=True)
    creator = UserGetSerializer(read_only=True)
    status = drf_serializers.CharField(read_only=True)
    order_code = drf_serializers.CharField(read_only=True)
    comment = drf_serializers.CharField(read_only=True)
    total_sum = drf_serializers.DecimalField(
        read_only=True, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES
    )

    class Meta:
        model = Order
        fields = (
            "uuid",
            "created_at",
            "creator",
            "status",
            "order_code",
            "comment",
            "total_sum",
        )


class OrderCreateSerializer(BaseProjectModelSerializer):
    order_code = drf_serializers.CharField(
        required=True, max_length=OrderConstants.ORDER_CODE_MAX_LENGTH
    )
    comment = drf_serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=OrderConstants.COMMENT_MAX_LENGTH,
        default="",
    )

    class Meta:
        model = Order
        fields = ("order_code", "comment")


class OrderUpdateSerializer(BaseProjectModelSerializer):
    status = drf_serializers.ChoiceField(
        required=False, choices=OrderConstants.STATUS_CHOICE
    )
    comment = drf_serializers.CharField(
        required=False, allow_blank=True, max_length=OrderConstants.COMMENT_MAX_LENGTH
    )

    class Meta:
        model = Order
        fields = ("status", "comment")
