from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import BlogPostsView, BlogPostView

urlpatterns = {
    path("blogPosts/", BlogPostsView.as_view(), name="blog_posts_list"),
    path("blogPosts/<int:pk>", BlogPostView.as_view(), name="single_blog_post"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
