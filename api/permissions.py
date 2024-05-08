from rest_framework import permissions


class IsLoggedUser(permissions.BasePermission):
    message = "Vous devez être connecté et être l'utilisateur en question pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: User
        user = request.user
        return user.is_authenticated and user == obj


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
