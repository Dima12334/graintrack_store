from django_filters import CharFilter, DateTimeFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from graintrack_store.orders.models import Order


class OrderFilterSet(FilterSet):
    status = CharFilter(lookup_expr="iexact")
    created_at_min = DateTimeFilter(lookup_expr="gte", field_name="created_at")
    created_at_max = DateTimeFilter(lookup_expr="lte", field_name="created_at")
    total_sum_min = NumberFilter(lookup_expr="gte", field_name="total_sum")
    total_sum_max = NumberFilter(lookup_expr="lte", field_name="total_sum")

    class Meta:
        model = Order
        field = [
            "status",
            "created_at_min",
            "created_at_max",
            "total_sum_min",
            "total_sum_max",
        ]
