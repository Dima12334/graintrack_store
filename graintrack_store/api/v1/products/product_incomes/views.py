from typing import Dict, Any

from rest_framework.generics import CreateAPIView, ListAPIView

from graintrack_store.api.v1.products.product_incomes.serializers import (
    ProductIncomeGetSerializer,
    ProductIncomeCreateSerializer,
)
from graintrack_store.core.adapters.services.products.product_income_service import (
    ProductIncomeService,
)
from graintrack_store.core.api.views import (
    ProjectCreateModelMixin,
    ProjectListModelMixin,
    ProjectGenericAPIView,
)
from graintrack_store.products.models import ProductIncome


class ProductIncomeView(
    ProjectCreateModelMixin,
    CreateAPIView,
    ProjectListModelMixin,
    ListAPIView,
    ProjectGenericAPIView,
):
    service = ProductIncomeService()
    serializer_class = ProductIncomeGetSerializer

    def get_serializer_class(self, *args, **kwargs):
        default = ProductIncomeGetSerializer
        __ = {
            "GET": ProductIncomeGetSerializer,
            "POST": ProductIncomeCreateSerializer,
        }
        return __.get(self.request.method, default)

    def create_object(self, validated_data: Dict[str, Any]) -> ProductIncome:
        return self.service.create_product_income(**validated_data)


product_income_view = ProductIncomeView.as_view()
