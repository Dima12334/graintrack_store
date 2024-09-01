from django.urls import path

from graintrack_store.api.v1.products.product_categories.views import (
    product_category_view,
    product_category_detail_view,
)
from graintrack_store.api.v1.products.product_discounts.views import (
    product_discount_view,
    product_discount_detail_view,
)
from graintrack_store.api.v1.products.product_incomes.views import product_income_view
from graintrack_store.api.v1.products.products.views import (
    product_detail_view,
    product_view,
)

app_name = "products"

urlpatterns = [
    path("", product_view),
    path("<uuid:uuid>/", product_detail_view),
    path("incomes/", product_income_view),
    path("categories/", product_category_view),
    path("categories/<uuid:uuid>/", product_category_detail_view),
    path("discounts/", product_discount_view),
    path("discounts/<uuid:uuid>/", product_discount_detail_view),
]
