from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

urlpatterns = [
    path(f"platform/{settings.ADMIN_URL}/", admin.site.urls),
    path("platform/oidc/", include("mozilla_django_oidc.urls")),
    path("platform/prose/", include("prose.urls")),
    path("platform/hijack/", include("hijack.urls")),
]
urlpatterns.append(re_path(r"^platform/", include(("web.urls", "web"), namespace="web")))
urlpatterns.append(re_path(r"^platform/", include("web.auth-urls")))
urlpatterns.append(re_path(r"^platform/api/v1/", include(("api.urls", "api"), namespace="api")))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_SILK:
    urlpatterns += [path("platform/silk/", include("silk.urls", namespace="silk"))]
