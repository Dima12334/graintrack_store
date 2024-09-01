from graintrack_store.core.api.serializers import BaseProjectModelSerializer
from graintrack_store.products.constants import ProductCategoryConstants
from graintrack_store.products.models import Product, ProductCategory
from rest_framework import serializers as drf_serializers


class ProductCategoryGetSerializer(BaseProjectModelSerializer):
    uuid = drf_serializers.UUIDField(read_only=True)
    created_at = drf_serializers.DateTimeField(read_only=True)
    name = drf_serializers.CharField(read_only=True)
    description = drf_serializers.CharField(read_only=True)
    parent_category_uuid = drf_serializers.UUIDField(
        read_only=True, source="parent_category.uuid", allow_null=True
    )

    class Meta:
        model = ProductCategory
        fields = ("uuid", "created_at", "name", "description", "parent_category_uuid")


class ProductCategoryCreateSerializer(BaseProjectModelSerializer):
    name = drf_serializers.CharField(
        required=True, max_length=ProductCategoryConstants.NAME_MAX_LENGTH
    )
    description = drf_serializers.CharField(
        required=False,
        default="",
        allow_blank=True,
        max_length=ProductCategoryConstants.DESCRIPTION_MAX_LENGTH,
    )
    parent_category = drf_serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = ProductCategory
        fields = ("name", "description", "parent_category")


class ProductCategoryUpdateSerializer(BaseProjectModelSerializer):
    name = drf_serializers.CharField(
        required=False, max_length=ProductCategoryConstants.NAME_MAX_LENGTH
    )
    description = drf_serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=ProductCategoryConstants.DESCRIPTION_MAX_LENGTH,
    )

    class Meta:
        model = ProductCategory
        fields = ("name", "description")
