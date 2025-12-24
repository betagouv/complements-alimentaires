from rest_framework import permissions

from data.models import ControlRole, Declaration, InstructionRole, VisaRole


class CanAccessUser(permissions.BasePermission):
    message = "Vous n'avez pas accès à cet utilisateur"

    def has_object_permission(self, request, view, obj):  # obj: User
        user = request.user
        is_agent = IsInstructor().has_permission(request, view) or IsVisor().has_permission(request, view)
        if user.is_authenticated and user == obj:
            return True
        return request.method in permissions.SAFE_METHODS and is_agent


class CanAccessUserDeclatarions(permissions.BasePermission):
    """
    Un.e utilisateur.ice peut avoir accès aux :
    - déclarations créées par iel même
    - déclarations d'une des compagnies pour lesquelles iel a droit de déclaration
    - déclarations d'une des compagnies pour lesquelles iel a droit de supervision
    """

    def has_object_permission(self, request, view, obj):  # obj est une déclaration
        created_by_user = obj.author == request.user
        if created_by_user:  # Pour éviter les requêtes successives si on n'a pas besoin
            return True

        declarable_companies = request.user.declarable_companies.all()
        supervisable_companies = request.user.supervisable_companies.all()
        companies = declarable_companies.union(supervisable_companies)

        user_has_company_roles = obj.company in companies or (
            obj.mandated_company and obj.mandated_company in companies
        )
        return user_has_company_roles

    def has_permission(self, request, view):
        return view.kwargs["user_pk"] == request.user.id


class IsSupervisor(permissions.BasePermission):
    message = "Vous devez être gestionnaire de cette entreprise pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: Company
        user = request.user
        return user.is_authenticated and obj.supervisor_roles.filter(user=user).exists()


class IsDeclarant(permissions.BasePermission):
    message = "Vous devez être déclarant de l'entreprise liée à cette déclaration pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: Declaration
        user = request.user
        companies = [obj.company] + list(obj.company.mandated_companies.all())
        return user.is_authenticated and any(company in user.declarable_companies.all() for company in companies)


class IsDeclarationAuthor(permissions.BasePermission):
    message = "Vous devez être l'auteur de cette déclaration pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: Declaration
        user = request.user
        return user.is_authenticated and obj.author == user


class IsSolicitationRecipient(permissions.BasePermission):
    message = "Vous devez être un des destinataires de cette demande pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: une Solicitation ayant un attribut recipients
        user = request.user
        return user.is_authenticated and user in obj.recipients.all()


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and InstructionRole.objects.filter(user=request.user).exists()


class IsVisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and VisaRole.objects.filter(user=request.user).exists()


class IsController(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and ControlRole.objects.filter(user=request.user).exists()


class IsSupervisorOrAgent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # obj: Company (for supervisor)
        user = request.user
        return user.is_authenticated and (
            IsSupervisor().has_object_permission(request, view, obj)
            or IsInstructor().has_permission(request, view)
            or IsVisor().has_permission(request, view)
        )


class CanAccessIndividualDeclaration(permissions.BasePermission):
    message = "Vous n'avez pas accès à cette déclaration"

    def has_object_permission(self, request, view, obj):  # obj: Declaration
        if not request.user.is_authenticated:
            return False
        is_agent = IsInstructor().has_permission(request, view) or IsVisor().has_permission(request, view)

        declarable_companies = request.user.declarable_companies.all()
        is_declarant_from_same_company = obj.company in declarable_companies or (
            obj.mandated_company and obj.mandated_company in declarable_companies
        )
        # le gestionnaire d'une entreprise a les droits de lecture seulement
        superviseable_companies = request.user.supervisable_companies.all()
        is_supervisor_from_same_company = obj.company in superviseable_companies or (
            obj.mandated_company and obj.mandated_company in superviseable_companies
        )

        is_draft = obj.status == Declaration.DeclarationStatus.DRAFT

        if request.method in permissions.SAFE_METHODS:
            return is_declarant_from_same_company or is_supervisor_from_same_company or (is_agent and not is_draft)

        return is_declarant_from_same_company or (is_agent and not is_draft)


class CanTakeAuthorship(permissions.BasePermission):
    message = "Vous ne pouvez pas vous assigner cette déclaration"

    def has_object_permission(self, request, view, obj):  # obj: Declaration
        if not request.user.is_authenticated:
            return False
        declarable_companies = request.user.declarable_companies.all()
        is_from_same_company = obj.company in declarable_companies
        is_from_mandated_company = obj.mandated_company and obj.mandated_company in declarable_companies
        is_declarant = IsDeclarant().has_object_permission(request, view, obj)

        return (is_from_same_company or is_from_mandated_company) and is_declarant
