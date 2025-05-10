from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
      title="API AI_INTERIOR",
      default_version='v1',
      description="Документація API AI_INTERIOR",
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[],
)

urlpatterns = [
    path('api/docs', schema_view.with_ui('swagger', cache_timeout=0)),

    path('admin/', admin.site.urls),
    path('api/ai-interior-gen/', include('interior_gen.urls')),
    path('api/', include('accounts.urls')),
]
