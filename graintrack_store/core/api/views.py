from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated


class ProjectGenericAPIView(GenericAPIView):
    """Default view"""

    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "uuid"

    def get_queryset(self):
        pass
