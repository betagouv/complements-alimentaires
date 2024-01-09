from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import api.views as views

urlpatterns = {
    path("blogPosts/", views.BlogPostsView.as_view(), name="blog_posts_list"),
    path("blogPosts/<int:pk>", views.BlogPostView.as_view(), name="single_blog_post"),
    path("subscribeNewsletter/", views.SubscribeNewsletter.as_view(), name="subscribe_newsletter"),
    path("loggedUser/", views.LoggedUserView.as_view(), name="logged_user"),
    path("webinars/", views.WebinarView.as_view(), name="webinar_list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("plants/<int:pk>", views.PlantRetrieveView.as_view(), name="single_plant"),
    path("ingredients/<int:pk>", views.IngredientRetrieveView.as_view(), name="single_ingredient"),
    path("microorganism/<int:pk>", views.MicroorganismRetrieveView.as_view(), name="single_microorganism"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
