from django_filters import BooleanFilter, DateTimeFilter
from django_filters.rest_framework import FilterSet

from graintrack_store.products.models import ProductDiscount


class ProductDiscountFilterSet(FilterSet):
    discount_started_at = DateTimeFilter(lookup_expr="gte")
    discount_ended_at = DateTimeFilter(lookup_expr="lte")
    is_active = BooleanFilter()

    class Meta:
        model = ProductDiscount
        fields = ["discount_started_at", "discount_ended_at", "is_active"]
