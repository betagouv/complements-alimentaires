"""
URL configuration for icare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.conf.urls import include
from web.views import VueAppDisplayView

urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns.append(re_path(r"", include("web.urls")))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# In order for vue-history to work in HTML5 mode, we need to add a catch-all
# route returning the app (https://router.vuejs.org/guide/essentials/history-mode.html#html5-history-mode)
urlpatterns.append(re_path(r"^.*/$", VueAppDisplayView.as_view()))
