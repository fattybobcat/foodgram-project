from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth.urls import urlpatterns
from django.urls import include, path

urlpatterns = [
    path("auth/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
