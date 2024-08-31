from typing import TypeVar, Dict, Any, List, Optional
from django.db.models import Model, QuerySet
from django_filters.rest_framework import FilterSet
from uuid import UUID


ModelType = TypeVar("ModelType", bound=Model, covariant=True)
FilterSetType = TypeVar("FilterSetType", bound=FilterSet, covariant=True)


class BaseRepository:
    model: ModelType
    filterset: Optional[FilterSetType] = None

    default_ordering = "-created_at"

    def get_base_qs(self):
        return self.model.objects.all()

    def list(self, filters: Dict[str, Any] = None) -> List[ModelType]:
        queryset = self.get_base_qs()

        if self.filterset and filters:
            filterset = self.filterset(filters, queryset)
            filterset.is_valid()
            queryset = filterset.qs
        queryset = queryset.order_by(self.default_ordering)

        return list(queryset)

    def retrieve_by_uuid(self, instance_uuid: UUID) -> Optional[ModelType]:
        queryset = self.get_base_qs()
        queryset = queryset.filter(uuid=instance_uuid)
        return queryset.first()

    def retrieve_by_id(self, instance_id: int) -> Optional[ModelType]:
        queryset = self.get_base_qs()
        queryset = queryset.filter(id=instance_id)
        return queryset.first()

    def delete(self, instance_uuid: UUID) -> bool:
        result = self.model.objects.filter(uuid=instance_uuid).delete()
        return result[0]
