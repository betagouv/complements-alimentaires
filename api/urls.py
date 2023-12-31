from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import BlogPostsView, BlogPostView, SubscribeNewsletter, LoggedUserView, WebinarView, SearchView

urlpatterns = {
    path("blogPosts/", BlogPostsView.as_view(), name="blog_posts_list"),
    path("blogPosts/<int:pk>", BlogPostView.as_view(), name="single_blog_post"),
    path("subscribeNewsletter/", SubscribeNewsletter.as_view(), name="subscribe_newsletter"),
    path("loggedUser/", LoggedUserView.as_view(), name="logged_user"),
    path("webinars/", WebinarView.as_view(), name="webinar_list"),
    path("search/", SearchView.as_view(), name="search"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
