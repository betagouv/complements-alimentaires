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
    path("units/", views.UnitListView.as_view(), name="unit_list"),
    path("declarations/", views.DeclarationCreateApiView.as_view(), name="create_declaration"),
    # Authentication
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # User
    path("get-logged-user/", views.LoggedUserView.as_view(), name="get_logged_user"),
    path("users/", views.UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>", views.UserUpdateDestroyView.as_view(), name="user_update_destroy"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("generate-username/", views.GenerateUsernameView.as_view(), name="generate_username"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify_email"),
    path(
        "send-new-signup-verification-email/<int:user_id>",
        views.SendNewSignupVerificationEmailView.as_view(),
        name="send_new_signup_verification_email",
    ),
    # Company
    path("countries/", views.CountryListView.as_view(), name="country_list"),
    path("check-siret/<str:siret>", views.CheckSiretView.as_view(), name="check_siret"),
    path(
        "claim-company-supervision/<str:siret>",
        views.ClaimCompanySupervisionView.as_view(),
        name="claim_company_supervision",
    ),
    path(
        "request-company-access/<str:siret>", views.RequestCompanyAccessView.as_view(), name="request_company_access"
    ),
    path("companies/", views.CompanyCreateView.as_view(), name="company_create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
