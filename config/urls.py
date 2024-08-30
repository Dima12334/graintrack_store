from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/v1/", include("graintrack_store.api.v1.urls")),
]


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


if settings.USE_DOCS:
    # YASG
    if "drf_yasg" in settings.INSTALLED_APPS:
        from drf_yasg import openapi
        from drf_yasg.views import get_schema_view
        from rest_framework import permissions

        schema_view = get_schema_view(
            openapi.Info(
                title="GRAINTRACK STORE API",
                default_version="1",
                description="GRAINTRACK STORE API",
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )
        urlpatterns += [
            path(
                r"api/docs/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            )
        ]
