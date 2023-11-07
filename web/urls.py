from django.urls import path
from web.views import VueAppDisplayView

urlpatterns = [
    path("", VueAppDisplayView.as_view(), name="app"),
]
