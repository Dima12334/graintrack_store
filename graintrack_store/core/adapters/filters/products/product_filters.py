from typing import List

from django_filters import UUIDFilter, CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet
from rest_framework.exceptions import ValidationError

from graintrack_store.products.models import Product, ProductCategory


class ProductFilterSet(FilterSet):
    category = UUIDFilter(method="filter_category")
    name = CharFilter(lookup_expr="icontains")
    price_min = NumberFilter(lookup_expr="gte", field_name="price")
    price_max = NumberFilter(lookup_expr="lte", field_name="price")

    class Meta:
        model = Product
        field = ["category", "name", "price_min", "price_max"]

    def get_descendant_categories(self, parent_category: ProductCategory) -> List[ProductCategory]:
        """
        Recursively get all descendant categories of a given category.
        """
        descendants = []
        for child in parent_category.child_categories.all():
            descendants.append(child)
            descendants.extend(self.get_descendant_categories(child))
        return descendants

    def filter_category(self, queryset, name, value):
        parent_category = ProductCategory.objects.filter(uuid=value).first()
        if not parent_category:
            raise ValidationError(f"Category with uuid {value} not found.")

        descendant_categories = self.get_descendant_categories(parent_category=parent_category)
        categories = [parent_category, *descendant_categories]

        return queryset.filter(category__in=categories)
