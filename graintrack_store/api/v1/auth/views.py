from django.contrib import auth
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from graintrack_store.api.v1.auth.serializers import LoginSerializer, UserSerializer, LogoutSerializer
from graintrack_store.core.api.views import ProjectGenericAPIView


class LoginAPIView(APIView):
    permission_classes = ()

    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        if request.user.is_authenticated:
            raise ValidationError(
                "Log in failure. You are already authenticated",
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = auth.authenticate(request, **serializer.validated_data)
        if user is not None:
            auth.login(user=user, request=request)
            context = {"request": request}
            serializer = UserSerializer(user, context=context)
            return Response(serializer.data)
        raise ValidationError("Log in failure. Please check your credentials")


login_api_view = LoginAPIView.as_view()


class LogoutAPIView(ProjectGenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request: Request):
        auth.logout(request)
        return Response({"message": "You successfully Logged Out"})


logout_api_view = LogoutAPIView.as_view()
