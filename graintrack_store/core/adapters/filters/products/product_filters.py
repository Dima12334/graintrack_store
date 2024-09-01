from typing import List

from django_filters import UUIDFilter, CharFilter, NumberFilter, DateTimeFilter
from django_filters.rest_framework import FilterSet
from rest_framework.exceptions import ValidationError

from graintrack_store.products.models import Product, ProductCategory


class CategoryFilterMixin:

    def get_descendant_categories(
        self, parent_category: ProductCategory
    ) -> List[ProductCategory]:
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

        descendant_categories = self.get_descendant_categories(
            parent_category=parent_category
        )
        categories = [parent_category, *descendant_categories]

        return queryset.filter(category__in=categories)


class ProductFilterSet(CategoryFilterMixin, FilterSet):
    name = CharFilter(lookup_expr="icontains")
    price_min = NumberFilter(lookup_expr="gte", field_name="price")
    price_max = NumberFilter(lookup_expr="lte", field_name="price")
    category = UUIDFilter(method="filter_category")

    class Meta:
        model = Product
        fields = ["name", "price_min", "price_max", "category"]


class SoldProductsReportFilterSet(CategoryFilterMixin, FilterSet):
    sold_at_min = DateTimeFilter(
        lookup_expr="gte", field_name="order_products__order__sold_at"
    )
    sold_at_max = DateTimeFilter(
        lookup_expr="lte", field_name="order_products__order__sold_at"
    )
    category = UUIDFilter(method="filter_category")

    class Meta:
        model = Product
        fields = ["sold_at_min", "sold_at_max", "category"]
