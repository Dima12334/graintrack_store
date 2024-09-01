from django.urls import path

from graintrack_store.api.v1.orders.order_products.views import (
    order_product_view,
    order_product_detail_view,
)
from graintrack_store.api.v1.orders.orders.views import order_view, order_detail_view

app_name = "orders"

urlpatterns = [
    path("", order_view),
    path("<uuid_hex:uuid>/", order_detail_view),
    path("products/", order_product_view),
    path("products/<uuid_hex:uuid>/", order_product_detail_view),
]
