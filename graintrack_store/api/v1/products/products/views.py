from typing import Dict, Any
from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)


from graintrack_store.api.v1.products.products.serializers import (
    ProductGetSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
)
from graintrack_store.core.adapters.filters.products.product_filters import (
    ProductFilterSet,
)
from graintrack_store.core.adapters.services.products.product_service import (
    ProductService,
)
from graintrack_store.core.api.views import (
    ProjectCreateModelMixin,
    ProjectListModelMixin,
    ProjectGenericAPIView,
    ProjectUpdateModelMixin,
    ProjectRetrieveModelMixin,
)
from graintrack_store.products.models import Product


class ProductView(
    ProjectCreateModelMixin,
    CreateAPIView,
    ProjectListModelMixin,
    ListAPIView,
    ProjectGenericAPIView,
):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilterSet

    service = ProductService()
    serializer_class = ProductGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductGetSerializer
        __ = {
            "GET": ProductGetSerializer,
            "POST": ProductCreateSerializer,
        }
        return __.get(self.request.method, default)

    def create_object(self, validated_data: Dict[str, Any]) -> Product:
        return self.service.create_product(**validated_data)


product_view = ProductView.as_view()


class ProductDetailView(
    ProjectUpdateModelMixin,
    UpdateAPIView,
    ProjectRetrieveModelMixin,
    RetrieveAPIView,
    ProjectGenericAPIView,
):
    service = ProductService()
    serializer_class = ProductGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductGetSerializer
        __ = {
            "GET": ProductGetSerializer,
            "PUT": ProductUpdateSerializer,
        }
        return __.get(self.request.method, default)

    def update_by_uuid(
        self, instance_uuid: UUID, validated_data: Dict[str, Any]
    ) -> Product:
        return self.service.update_product(instance_uuid, **validated_data)


product_detail_view = ProductDetailView.as_view()
