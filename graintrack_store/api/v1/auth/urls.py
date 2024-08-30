from django.urls import path

from graintrack_store.api.v1.auth.views import login_api_view, logout_api_view

app_name = "auth"

urlpatterns = [
    path("session/login/", login_api_view),
    path("session/logout/", logout_api_view),
]
