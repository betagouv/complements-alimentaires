import logging
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import BlogPostSerializer
from data.models import BlogPost
from django_filters import rest_framework as django_filters
from django.db.models.constants import LOOKUP_SEP
from rest_framework import filters

logger = logging.getLogger(__name__)


class UnaccentSearchFilter(filters.SearchFilter):
    def construct_search(self, field_name, _):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = "icontains"
        return LOOKUP_SEP.join(
            [
                field_name,
                "unaccent",
                lookup,
            ]
        )


class BlogPostsPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30


class BlogPostsView(ListAPIView):
    model = BlogPost
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True)
    pagination_class = BlogPostsPagination
    filter_backends = [django_filters.DjangoFilterBackend, UnaccentSearchFilter]
    search_fields = ["title", "tagline", "content"]


class BlogPostView(RetrieveAPIView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
