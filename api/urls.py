from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import api.views as views

urlpatterns = {
    path("blogPosts/", views.BlogPostsView.as_view(), name="blog_posts_list"),
    path("blogPosts/<int:pk>", views.BlogPostView.as_view(), name="single_blog_post"),
    path("subscribeNewsletter/", views.SubscribeNewsletter.as_view(), name="subscribe_newsletter"),
    path("reportIssue/", views.ReportIssue.as_view(), name="report_issue"),
    path("webinars/", views.WebinarView.as_view(), name="webinar_list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("plants/<int:pk>", views.PlantRetrieveView.as_view(), name="single_plant"),
    path("plantParts/", views.PlantPartListView.as_view(), name="plant_part_list"),
    path("ingredients/<int:pk>", views.IngredientRetrieveView.as_view(), name="single_ingredient"),
    path("microorganisms/<int:pk>", views.MicroorganismRetrieveView.as_view(), name="single_microorganism"),
    path("substances/<int:pk>", views.SubstanceRetrieveView.as_view(), name="single_substance"),
    path("elements/autocomplete/", views.AutocompleteView.as_view(), name="substance_autocomplete"),
    path("populations/", views.PopulationListView.as_view(), name="population_list"),
    path("conditions/", views.ConditionListView.as_view(), name="condition_list"),
    # Authentication
    path("loggedUser/", views.LoggedUserView.as_view(), name="logged_user"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
