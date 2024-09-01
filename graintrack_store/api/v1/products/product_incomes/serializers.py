from graintrack_store.api.v1.products.products.serializers import ProductGetSerializer
from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.products.models import ProductIncome
from rest_framework import serializers as drf_serializers


class ProductIncomeGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    created_at = drf_serializers.DateTimeField(read_only=True)
    product = ProductGetSerializer(read_only=True)
    quantity = drf_serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductIncome
        fields = ("uuid", "created_at", "product", "quantity")


class ProductIncomeCreateSerializer(BaseProjectModelSerializer):
    product = drf_serializers.UUIDField(required=True)
    quantity = drf_serializers.IntegerField(required=True)

    class Meta:
        model = ProductIncome
        fields = ("product", "quantity")
