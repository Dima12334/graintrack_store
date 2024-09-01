from typing import Dict, Any
from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)


from graintrack_store.api.v1.products.product_discounts.serializers import (
    ProductDiscountUpdateSerializer,
    ProductDiscountGetSerializer,
    ProductDiscountCreateSerializer,
)
from graintrack_store.core.adapters.filters.products.product_discount_filters import (
    ProductDiscountFilterSet,
)
from graintrack_store.core.adapters.services.products.product_discount_service import (
    ProductDiscountService,
)
from graintrack_store.core.api.views import (
    ProjectCreateModelMixin,
    ProjectListModelMixin,
    ProjectGenericAPIView,
    ProjectUpdateModelMixin,
    ProjectRetrieveModelMixin,
)
from graintrack_store.products.models import ProductCategory, ProductDiscount


class ProductDiscountView(
    ProjectCreateModelMixin,
    CreateAPIView,
    ProjectListModelMixin,
    ListAPIView,
    ProjectGenericAPIView,
):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductDiscountFilterSet

    service = ProductDiscountService()
    serializer_class = ProductDiscountGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductDiscountGetSerializer
        __ = {
            "GET": ProductDiscountGetSerializer,
            "POST": ProductDiscountCreateSerializer,
        }
        return __.get(self.request.method, default)

    def create_object(self, validated_data: Dict[str, Any]) -> ProductDiscount:
        return self.service.create_product_discount(**validated_data)


product_discount_view = ProductDiscountView.as_view()


class ProductDiscountDetailView(
    ProjectUpdateModelMixin,
    UpdateAPIView,
    ProjectRetrieveModelMixin,
    RetrieveAPIView,
    ProjectGenericAPIView,
):
    service = ProductDiscountService()
    serializer_class = ProductDiscountGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductDiscountGetSerializer
        __ = {
            "GET": ProductDiscountGetSerializer,
            "PUT": ProductDiscountUpdateSerializer,
        }
        return __.get(self.request.method, default)

    def update_by_uuid(
        self, instance_uuid: UUID, validated_data: Dict[str, Any]
    ) -> ProductDiscount:
        return self.service.update_product_discount(instance_uuid, **validated_data)


product_discount_detail_view = ProductDiscountDetailView.as_view()
