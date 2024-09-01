from typing import Dict, Any
from uuid import UUID

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)

from graintrack_store.api.v1.products.product_categories.serializers import (
    ProductCategoryGetSerializer,
    ProductCategoryCreateSerializer,
    ProductCategoryUpdateSerializer,
)
from graintrack_store.core.adapters.services.products.product_category_service import (
    ProductCategoryService,
)
from graintrack_store.core.api.views import (
    ProjectCreateModelMixin,
    ProjectListModelMixin,
    ProjectGenericAPIView,
    ProjectUpdateModelMixin,
    ProjectRetrieveModelMixin,
)
from graintrack_store.products.models import ProductCategory


class ProductCategoryView(
    ProjectCreateModelMixin,
    CreateAPIView,
    ProjectListModelMixin,
    ListAPIView,
    ProjectGenericAPIView,
):
    service = ProductCategoryService()
    serializer_class = ProductCategoryGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductCategoryGetSerializer
        __ = {
            "GET": ProductCategoryGetSerializer,
            "POST": ProductCategoryCreateSerializer,
        }
        return __.get(self.request.method, default)

    def create_object(self, validated_data: Dict[str, Any]) -> ProductCategory:
        return self.service.create_product_category(**validated_data)


product_category_view = ProductCategoryView.as_view()


class ProductCategoryDetailView(
    ProjectUpdateModelMixin,
    UpdateAPIView,
    ProjectRetrieveModelMixin,
    RetrieveAPIView,
    ProjectGenericAPIView,
):
    service = ProductCategoryService()
    serializer_class = ProductCategoryGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductCategoryGetSerializer
        __ = {
            "GET": ProductCategoryGetSerializer,
            "PUT": ProductCategoryUpdateSerializer,
        }
        return __.get(self.request.method, default)

    def update_by_uuid(
        self, instance_uuid: UUID, validated_data: Dict[str, Any]
    ) -> ProductCategory:
        return self.service.update_product_category(instance_uuid, **validated_data)


product_category_detail_view = ProductCategoryDetailView.as_view()
