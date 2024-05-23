from rest_framework import permissions

from data.models import Declaration, InstructionRole


class CanAccessUser(permissions.BasePermission):
    message = "Vous n'avez pas accès à cet utilisateur"

    def has_object_permission(self, request, view, obj):  # obj: User
        user = request.user
        is_instructor = IsInstructor().has_permission(request, view)
        if user.is_authenticated and user == obj:
            return True
        return request.method in permissions.SAFE_METHODS and is_instructor


class CanAccessUserDeclatarions(permissions.BasePermission):
    """
    Un.e utilisateur.ice peut seulement avoir accès à ces propres déclarations. Cette
    permission vérifie que le paramètre dans l'URL `user_pk` corresponde à l'objet
    `user` de la requête.
    """

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
        return user.is_authenticated and obj.company.declarant_roles.filter(user=user).exists()


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
        return InstructionRole.objects.filter(user=request.user).exists()


class CanAccessIndividualDeclaration(permissions.BasePermission):
    message = "Vous n'avez pas accès à cette déclaration"

    def has_object_permission(self, request, view, obj):  # obj: Declaration
        is_author = IsDeclarationAuthor().has_object_permission(request, view, obj)
        is_instructor = IsInstructor().has_permission(request, view)
        is_declarant = IsDeclarant().has_object_permission(request, view, obj)
        is_draft = obj.status == Declaration.DeclarationStatus.DRAFT
        if request.method in permissions.SAFE_METHODS:
            return is_author or (is_instructor and not is_draft)

        return is_author and is_declarant
