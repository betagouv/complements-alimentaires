from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from web.views import VueAppDisplayView

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("prose/", include("prose.urls")),
    path("hijack/", include("hijack.urls")),
]
urlpatterns.append(re_path(r"", include(("web.urls", "web"), namespace="web")))
urlpatterns.append(re_path(r"", include("web.auth-urls")))
urlpatterns.append(re_path(r"^api/v1/", include(("api.urls", "api"), namespace="api")))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

# In order for vue-history to work in HTML5 mode, we need to add a catch-all
# route returning the app (https://router.vuejs.org/guide/essentials/history-mode.html#html5-history-mode)
urlpatterns.append(re_path(r"^.*/$", VueAppDisplayView.as_view()))
