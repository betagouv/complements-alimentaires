from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

# TODO spinal-casify old camelCase routes
urlpatterns = {
    path("blog-post/", views.BlogPostsView.as_view(), name="blog_posts_list"),
    path("blog-post/<int:pk>", views.BlogPostView.as_view(), name="single_blog_post"),
    path("subscribe-newsletter/", views.SubscribeNewsletter.as_view(), name="subscribe_newsletter"),
    path("report-issue/", views.ReportIssue.as_view(), name="report_issue"),
    path("webinars/", views.WebinarView.as_view(), name="webinar_list"),
    # Elements
    path("search/", views.SearchView.as_view(), name="search"),
    path("plants/<int:pk>", views.PlantRetrieveView.as_view(), name="single_plant"),
    path("plant-parts/", views.PlantPartListView.as_view(), name="plant_part_list"),
    path("ingredients/<int:pk>", views.IngredientRetrieveView.as_view(), name="single_ingredient"),
    path("microorganisms/<int:pk>", views.MicroorganismRetrieveView.as_view(), name="single_microorganism"),
    path("substances/<int:pk>", views.SubstanceRetrieveView.as_view(), name="single_substance"),
    path("elements/autocomplete/", views.AutocompleteView.as_view(), name="substance_autocomplete"),
    # References
    path("populations/", views.PopulationListView.as_view(), name="population_list"),
    path("conditions/", views.ConditionListView.as_view(), name="condition_list"),
    path("effects/", views.EffectListView.as_view(), name="effect_list"),
    path("galenic-formulation/", views.GalenicFormulationListView.as_view(), name="galenic_formulation_list"),
    path("units/", views.UnitListView.as_view(), name="unit_list"),
    # Authentication
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # User
    path("get-logged-user/", views.LoggedUserView.as_view(), name="get_logged_user"),
    path("users/", views.UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>", views.UserRetrieveUpdateDestroyView.as_view(), name="user_retrieve_update_destroy"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("generate-username/", views.GenerateUsernameView.as_view(), name="generate_username"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify_email"),
    path(
        "send-new-signup-verification-email/<int:user_id>",
        views.SendNewSignupVerificationEmailView.as_view(),
        name="send_new_signup_verification_email",
    ),
    # Roles
    path("users/<int:user_pk>/add-role/", views.AddCompanyRoleView.as_view(), name="add_role"),
    path("users/<int:user_pk>/remove-role/", views.RemoveCompanyRoleView.as_view(), name="remove_role"),
    # Company
    path("countries/", views.CountryListView.as_view(), name="country_list"),
    path("companies/", views.CompanyCreateView.as_view(), name="company_create"),
    path("companies/<int:pk>", views.CompanyRetrieveUpdateView.as_view(), name="company_retrieve_update"),
    path(
        "companies/<int:pk>/collaborators",
        views.CompanyCollaboratorsListView.as_view(),
        name="get_company_collaborators",
    ),
    path(
        "companies/<str:identifier>/check-identifier/",
        views.CheckCompanyIdentifierView.as_view(),
        name="check_company_identifier",
    ),
    path(
        "companies/<str:identifier>/claim-supervision/",
        views.ClaimCompanySupervisionView.as_view(),
        name="claim_company_supervision",
    ),
    path(
        "companies/<str:identifier>/claim-co-supervision/",
        views.ClaimCompanyCoSupervisionView.as_view(),
        name="claim_company_co_supervision",
    ),
    path(
        "companies/<int:pk>/add-new-collaborator/",
        views.AddNewCollaboratorView.as_view(),
        name="add_new_collaborator",
    ),
    # Solicitations
    path(
        "companies/<int:pk>/collaboration-invitations/",
        views.CollaborationInvitationListView.as_view(),
        name="list_collaboration_invitation",
    ),
    path(
        "companies/<int:pk>/co-supervision-claims/",
        views.CoSupervisionClaimListView.as_view(),
        name="list_co_supervision_claim",
    ),
    path(
        "co-supervision-claims/<int:pk>/process/",
        views.ProcessCoSupervisionClaim.as_view(),
        name="process_co_supervision_claim",
    ),
    # Declarations
    path(
        "users/<int:user_pk>/declarations/",
        views.UserDeclarationsListCreateApiView.as_view(),
        name="list_create_declaration",
    ),
    path("declarations/", views.AllDeclarationsListView.as_view(), name="list_all_declarations"),
    path("declarations/<int:pk>", views.DeclarationRetrieveUpdateView.as_view(), name="retrieve_update_declaration"),
    path("declarations/<int:pk>/submit/", views.DeclarationSubmitView.as_view(), name="submit_declaration"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
