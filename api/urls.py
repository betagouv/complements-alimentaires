from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

import api.views as views

# TODO spinal-casify old camelCase routes
urlpatterns = {
    path("blog-post/", views.BlogPostsView.as_view(), name="blog_posts_list"),
    path("blog-post/<int:pk>", views.BlogPostView.as_view(), name="single_blog_post"),
    path("subscribe-newsletter/", views.SubscribeNewsletter.as_view(), name="subscribe_newsletter"),
    path("report-issue/", views.ErrorReportCreateView.as_view(), name="report_issue"),
    path("webinars/", views.WebinarView.as_view(), name="webinar_list"),
    # Ingredients
    path("search/", views.SearchView.as_view(), name="search"),
    path("plants/", views.PlantCreateView.as_view(), name="plant_create"),
    path("plants/<int:pk>", views.PlantRetrieveUpdateView.as_view(), name="single_plant"),
    path("plant-parts/", views.PlantPartListView.as_view(), name="plant_part_list"),
    path("plant-families/", views.PlantFamilyListView.as_view(), name="plant_family_list"),
    path("other-ingredients/", views.IngredientCreateView.as_view(), name="ingredient_create"),
    path("other-ingredients/<int:pk>", views.IngredientRetrieveUpdateView.as_view(), name="single_ingredient"),
    path("microorganisms/", views.MicroorganismCreateView.as_view(), name="microorganism_create"),
    path("microorganisms/<int:pk>", views.MicroorganismRetrieveUpdateView.as_view(), name="single_microorganism"),
    path("substances/", views.SubstanceCreateView.as_view(), name="substance_create"),
    path("substances/<int:pk>", views.SubstanceRetrieveUpdateView.as_view(), name="single_substance"),
    path("elements/autocomplete/", views.AutocompleteView.as_view(), name="element_autocomplete"),
    # Declared elements
    path("new-declared-elements/", views.DeclaredElementsView.as_view(), name="list_new_declared_elements"),
    path("declared-elements/<str:type>/<int:pk>", views.DeclaredElementView.as_view(), name="declared_element"),
    path(
        "declared-elements/<str:type>/<int:pk>/request-info",
        views.DeclaredElementRequestInfoView.as_view(),
        name="declared_element_request_info",
    ),
    path(
        "declared-elements/<str:type>/<int:pk>/reject",
        views.DeclaredElementRejectView.as_view(),
        name="declared_element_reject",
    ),
    path(
        "declared-elements/<str:type>/<int:pk>/replace",
        views.DeclaredElementReplaceView.as_view(),
        name="declared_element_replace",
    ),
    path(
        "declared-elements/<str:type>/<int:pk>/accept-part",
        views.DeclaredElementAcceptPartView.as_view(),
        name="declared_element_accept_part",
    ),
    # References
    path("populations/", views.PopulationListView.as_view(), name="population_list"),
    path("conditions/", views.ConditionListView.as_view(), name="condition_list"),
    path("effects/", views.EffectListView.as_view(), name="effect_list"),
    path("galenic-formulations/", views.GalenicFormulationListView.as_view(), name="galenic_formulation_list"),
    path("preparations/", views.PreparationListView.as_view(), name="preparation_list"),
    path("units/", views.UnitListView.as_view(), name="unit_list"),
    path("declarationFieldData/", views.DeclarationFieldsGroupedView.as_view(), name="declaration_field_data"),
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
        "companies/<int:pk>/declarations/",
        views.CompanyDeclarationsListView.as_view(),
        name="company_declarations_list_view",
    ),
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
        "companies/<int:pk>/claim-company-access/",
        views.ClaimCompanyAccessView.as_view(),
        name="claim_company_access",
    ),
    path(
        "companies/<int:pk>/add-new-collaborator/",
        views.AddNewCollaboratorView.as_view(),
        name="add_new_collaborator",
    ),
    # Entreprises mandatées
    path(
        "companies/<int:pk>/add-mandated-company/", views.AddMandatedCompanyView.as_view(), name="add_mandated_company"
    ),
    path(
        "companies/<int:pk>/remove-mandated-company/",
        views.RemoveMandatedCompanyView.as_view(),
        name="remove_mandated_company",
    ),
    # Solicitations
    path(
        "companies/<int:pk>/collaboration-invitations/",
        views.CollaborationInvitationListView.as_view(),
        name="list_collaboration_invitation",
    ),
    path(
        "companies/<int:pk>/company-access-claims/",
        views.CompanyAccessClaimListView.as_view(),
        name="list_company_access_claim",
    ),
    path(
        "company-access-claims/<int:pk>/process/",
        views.ProcessCompanyAccessClaim.as_view(),
        name="process_company_access_claim",
    ),
    # Declarations
    path(
        "users/<int:user_pk>/declarations/",
        views.UserDeclarationsListCreateApiView.as_view(),
        name="list_create_declaration",
    ),
    path("declarations/", views.OngoingDeclarationsListView.as_view(), name="list_all_declarations"),
    path("control/declarations/", views.ControllerDeclarationsListView.as_view(), name="list_control_declarations"),
    path(
        "control/declarations/<int:pk>",
        views.ControllerDeclarationRetrieveView.as_view(),
        name="retrieve_control_declaration",
    ),
    path("control/companies/", views.ControlCompanyListView.as_view(), name="list_control_companies"),
    path("control/companies-export/", views.ControlCompanyExcelView.as_view(), name="export_excel_companies_control"),
    path("control/companies/<int:pk>", views.CompanyControlRetrieveView.as_view(), name="retrieve_control_company"),
    path("control/users/<int:pk>", views.UserRetrieveControlView.as_view(), name="retrieve_control_user"),
    path("declarations-export/", views.OngoingDeclarationsExcelView.as_view(), name="export_excel_declarations"),
    path(
        "declarations/<int:pk>",
        views.DeclarationRetrieveUpdateDestroyView.as_view(),
        name="retrieve_update_destroy_declaration",
    ),
    path(
        "declarations/<int:pk>/snapshots/",
        views.DeclarationSnapshotListView.as_view(),
        name="declaration_snapshots",
    ),
    path(
        "declarations/<int:pk>/update-article/",
        views.ArticleChangeView.as_view(),
        name="update_article",
    ),
    path(
        "declarations/<int:pk>/take-authorship/",
        views.DeclarationTakeAuthorshipView.as_view(),
        name="take_authorship",
    ),
    path(
        "declarations/<int:pk>/assign-instruction/",
        views.DeclarationAssignInstruction.as_view(),
        name="assign_instruction",
    ),
    # Flow de la déclaration (state machine)
    path("declarations/<int:pk>/submit/", views.DeclarationSubmitView.as_view(), name="submit_declaration"),
    path(
        "declarations/<int:pk>/take-for-instruction/",
        views.DeclarationTakeForInstructionView.as_view(),
        name="take_for_instruction",
    ),
    path(
        "declarations/<int:pk>/take-for-visa/",
        views.DeclarationTakeForVisaView.as_view(),
        name="take_for_visa",
    ),
    path(
        "declarations/<int:pk>/observe-no-visa/",
        views.DeclarationObserveView.as_view(),
        name="observe_no_visa",
    ),
    path(
        "declarations/<int:pk>/authorize-no-visa/",
        views.DeclarationAuthorizeView.as_view(),
        name="authorize_no_visa",
    ),
    path(
        "declarations/<int:pk>/resubmit/",
        views.DeclarationResubmitView.as_view(),
        name="resubmit_declaration",
    ),
    path(
        "declarations/<int:pk>/observe-with-visa/",
        views.DeclarationObserveWithVisa.as_view(),
        name="observe_with_visa",
    ),
    path(
        "declarations/<int:pk>/object-with-visa/", views.DeclarationObjectWithVisa.as_view(), name="object_with_visa"
    ),
    path(
        "declarations/<int:pk>/reject-with-visa/", views.DeclarationRejectWithVisa.as_view(), name="reject_with_visa"
    ),
    path(
        "declarations/<int:pk>/authorize-with-visa/",
        views.DeclarationAuthorizeWithVisa.as_view(),
        name="authorize_with_visa",
    ),
    path(
        "declarations/<int:pk>/refuse-visa/",
        views.DeclarationRefuseVisaView.as_view(),
        name="refuse_visa",
    ),
    path(
        "declarations/<int:pk>/accept-visa/",
        views.DeclarationAcceptVisaView.as_view(),
        name="accept_visa",
    ),
    path(
        "declarations/<int:pk>/withdraw/",
        views.DeclarationWithdrawView.as_view(),
        name="withdraw",
    ),
    path(
        "declarations/<int:pk>/abandon/",
        views.DeclarationAbandonView.as_view(),
        name="abandon",
    ),
    # Contact
    path("contact/", views.ContactView.as_view(), name="contact"),
    # Stats
    path("stats/", views.StatsView.as_view(), name="stats"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
