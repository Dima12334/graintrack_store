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
from rest_framework.mixins import DestroyModelMixin

from graintrack_store.api.v1.orders.orders.serializers import (
    OrderGetSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
)
from graintrack_store.core.adapters.filters.orders.order_filters import OrderFilterSet
from graintrack_store.core.adapters.services.orders.order_service import OrderService
from graintrack_store.core.api.views import (
    ProjectCreateModelMixin,
    ProjectListModelMixin,
    ProjectGenericAPIView,
    ProjectUpdateModelMixin,
    ProjectRetrieveModelMixin,
    ProjectDestroyModelMixin,
)
from graintrack_store.orders.models import Order


class OrderView(
    ProjectCreateModelMixin,
    CreateAPIView,
    ProjectListModelMixin,
    ListAPIView,
    ProjectGenericAPIView,
):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilterSet

    service = OrderService()
    serializer_class = OrderGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = OrderGetSerializer
        __ = {
            "GET": OrderGetSerializer,
            "POST": OrderCreateSerializer,
        }
        return __.get(self.request.method, default)

    def create_object(self, validated_data: Dict[str, Any]) -> Order:
        return self.service.create_order(**validated_data)


order_view = OrderView.as_view()


class OrderDetailView(
    ProjectUpdateModelMixin,
    UpdateAPIView,
    ProjectRetrieveModelMixin,
    RetrieveAPIView,
    ProjectDestroyModelMixin,
    DestroyAPIView,
    ProjectGenericAPIView,
):
    service = OrderService()
    serializer_class = OrderGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = OrderGetSerializer
        __ = {
            "GET": OrderGetSerializer,
            "PUT": OrderUpdateSerializer,
        }
        return __.get(self.request.method, default)

    def update_by_uuid(
        self, instance_uuid: UUID, validated_data: Dict[str, Any]
    ) -> Order:
        return self.service.update_order(instance_uuid, **validated_data)

    def perform_destroy(self, instance_uuid: UUID):
        return self.service.delete_order(instance_uuid)


order_detail_view = OrderDetailView.as_view()
