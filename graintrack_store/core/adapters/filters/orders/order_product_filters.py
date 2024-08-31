from django_filters import UUIDFilter
from django_filters.rest_framework import FilterSet

from graintrack_store.orders.models import OrderProduct


class OrderProductFilterSet(FilterSet):
    order = UUIDFilter(field_name="order__uuid")
    product = UUIDFilter(field_name="product__uuid")

    class Meta:
        model = OrderProduct
        field = ["order", "product"]
