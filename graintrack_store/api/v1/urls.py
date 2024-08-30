from django.urls import path, include

urlpatterns = [
    path("auth/", include("graintrack_store.api.v1.auth.urls")),
    # path("products/", include("graintrack_store.api.v1.products.urls")),
    # path("sales/", include("graintrack_store.api.v1.sales.urls")),
]