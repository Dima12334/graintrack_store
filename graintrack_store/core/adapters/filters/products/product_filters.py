from django_filters import UUIDFilter, CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from graintrack_store.products.models import Product


class ProductFilterSet(FilterSet):
    category = UUIDFilter(field_name="category__uuid")
    name = CharFilter(lookup_expr="icontains")
    price_min = NumberFilter(lookup_expr="gte", field_name="price")
    price_max = NumberFilter(lookup_expr="lte", field_name="price")

    class Meta:
        model = Product
        field = ["category", "name", "price_min", "price_max"]
