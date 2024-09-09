from typing import List, Dict, Any
from uuid import UUID

from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from graintrack_store.core.adapters.repositories.base import ModelType
from graintrack_store.core.adapters.services.base import BaseService


class ProjectGenericAPIView(GenericAPIView):
    """Default view"""

    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "uuid"

    def get_queryset(self):
        pass


class ProjectListModelMixin(ListModelMixin):
    service: BaseService = None

    def list(self, request, *args, **kwargs) -> Response:
        filters = request.query_params.copy()
        instances = self.service.list(filters=filters, user=request.user)

        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ProjectUpdateModelMixin(UpdateModelMixin):

    def update_by_uuid(
        self, instance_uuid: UUID, validated_data: Dict[str, Any]
    ) -> ModelType:
        raise NotImplementedError

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance_uuid = self.kwargs.get(self.lookup_url_kwarg)
        instance = self.update_by_uuid(instance_uuid, serializer.validated_data)
        serialized_instance = self.serializer_class(instance=instance)

        return Response(serialized_instance.data, status=HTTP_200_OK)


class ProjectCreateModelMixin(CreateModelMixin):

    def create_object(self, validated_data: Dict[str, Any]) -> ModelType:
        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.create_object(serializer.validated_data)
        headers = self.get_success_headers(serializer.validated_data)
        serialized_instance = self.serializer_class(instance=instance)

        return Response(
            serialized_instance.data, status=HTTP_201_CREATED, headers=headers
        )


class ProjectDestroyModelMixin(DestroyModelMixin):

    def perform_destroy(self, instance_uuid: UUID):
        raise NotImplementedError

    def destroy(self, request, *args, **kwargs):
        instance_uuid = self.kwargs.get(self.lookup_url_kwarg)
        self.perform_destroy(instance_uuid)
        return Response(status=HTTP_204_NO_CONTENT)


class ProjectRetrieveModelMixin(RetrieveModelMixin):
    service: BaseService = None

    def get_object(self) -> ModelType:
        uuid = self.kwargs.get(self.lookup_url_kwarg)
        obj = self.service.retrieve(uuid=uuid)
        if not obj:
            raise Http404("Object not found")
        return obj
