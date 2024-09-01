from typing import Dict, Any
from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from graintrack_store.api.v1.orders.order_products.serializers import (
    OrderProductUpdateSerializer,
    OrderProductGetSerializer,
    OrderProductCreateSerializer,
)
from graintrack_store.core.adapters.filters.orders.order_product_filters import (
    OrderProductFilterSet,
)
from graintrack_store.core.adapters.services.orders.order_product_service import (
    OrderProductService,
)
from graintrack_store.core.api.views import (
    ProjectCreateModelMixin,
    ProjectListModelMixin,
    ProjectGenericAPIView,
    ProjectUpdateModelMixin,
    ProjectRetrieveModelMixin,
    ProjectDestroyModelMixin,
)
from graintrack_store.orders.models import Order, OrderProduct


class OrderProductView(
    ProjectCreateModelMixin,
    CreateAPIView,
    ProjectListModelMixin,
    ListAPIView,
    ProjectGenericAPIView,
):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderProductFilterSet

    service = OrderProductService()
    serializer_class = OrderProductGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = OrderProductGetSerializer
        __ = {
            "GET": OrderProductGetSerializer,
            "POST": OrderProductCreateSerializer,
        }
        return __.get(self.request.method, default)

    def create_object(self, validated_data: Dict[str, Any]) -> OrderProduct:
        return self.service.create_order_product(**validated_data)

    def list(self, request, *args, **kwargs) -> Response:
        filters = request.query_params.copy()
        instances = self.service.list_order_products(user=request.user, filters=filters)

        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


order_product_view = OrderProductView.as_view()


class OrderProductDetailView(
    ProjectUpdateModelMixin,
    UpdateAPIView,
    ProjectRetrieveModelMixin,
    RetrieveAPIView,
    ProjectDestroyModelMixin,
    DestroyAPIView,
    ProjectGenericAPIView,
):
    service = OrderProductService()
    serializer_class = OrderProductGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = OrderProductGetSerializer
        __ = {
            "GET": OrderProductGetSerializer,
            "PUT": OrderProductUpdateSerializer,
        }
        return __.get(self.request.method, default)

    def update_by_uuid(
        self, instance_uuid: UUID, validated_data: Dict[str, Any]
    ) -> OrderProduct:
        return self.service.update_order_product(instance_uuid, **validated_data)

    def perform_destroy(self, instance_uuid: UUID):
        return self.service.delete_order_product(instance_uuid)


order_product_detail_view = OrderProductDetailView.as_view()
