from .authentication import LoginView, LogoutView
from .autocomplete import AutocompleteView
from .blog import BlogPostsView, BlogPostView
from .condition import ConditionListView
from .declaration.declaration import (
    UserDeclarationsListCreateApiView,
    DeclarationRetrieveUpdateDestroyView,
    DeclarationSubmitView,
    OngoingDeclarationsExcelView,
    OngoingDeclarationsListView,
    ControllerDeclarationsListView,
    ControllerDeclarationRetrieveView,
    CompanyDeclarationsListView,
    DeclarationTakeForInstructionView,
    DeclarationTakeForVisaView,
    DeclarationObserveView,
    DeclarationAuthorizeView,
    DeclarationResubmitView,
    DeclarationAbandonView,
    DeclarationObserveWithVisa,
    DeclarationObjectWithVisa,
    DeclarationRejectWithVisa,
    DeclarationAuthorizeWithVisa,
    DeclarationRefuseVisaView,
    DeclarationAcceptVisaView,
    DeclarationWithdrawView,
    DeclarationTakeAuthorshipView,
    DeclarationAssignInstruction,
    ArticleChangeView,
    ControlDeclataionExcelView,
)
from .declaration.declared_element import (
    DeclaredElementsView,
    DeclaredElementView,
    DeclaredElementRequestInfoView,
    DeclaredElementRejectView,
    DeclaredElementReplaceView,
    DeclaredElementAcceptPartView,
)
from .effect import EffectListView
from .galenic_formulation import GalenicFormulationListView
from .preparation import PreparationListView
from .ingredient import IngredientRetrieveUpdateView, IngredientCreateView
from .microorganism import MicroorganismRetrieveUpdateView, MicroorganismCreateView
from .newsletter import SubscribeNewsletter
from .plant import PlantPartListView, PlantRetrieveUpdateView, PlantCreateView, PlantFamilyListView
from .population import PopulationListView
from .search import SearchView
from .substance import SubstanceRetrieveUpdateView, SubstanceCreateView
from .unit import UnitListView
from .user import (
    ChangePasswordView,
    GenerateUsernameView,
    LoggedUserView,
    SendNewSignupVerificationEmailView,
    UserCreateView,
    UserRetrieveUpdateDestroyView,
    UserRetrieveControlView,
    VerifyEmailView,
)
from .webinar import WebinarView

from .company import (
    CheckCompanyIdentifierView,
    ClaimCompanyAccessView,
    ClaimCompanySupervisionView,
    CompanyCreateView,
    CompanyRetrieveUpdateView,
    CountryListView,
    CompanyCollaboratorsListView,
    AddCompanyRoleView,
    RemoveCompanyRoleView,
    AddMandatedCompanyView,
    RemoveMandatedCompanyView,
    ControlCompanyListView,
    CompanyControlRetrieveView,
    ControlCompanyExcelView,
)
from .solicitation import (
    ProcessCompanyAccessClaim,
    CompanyAccessClaimListView,
    CollaborationInvitationListView,
    AddNewCollaboratorView,
)
from .snapshot import DeclarationSnapshotListView
from .grouped_views import DeclarationFieldsGroupedView
from .contact import ContactView
from .error_report import ErrorReportCreateView
from .stats import StatsView
