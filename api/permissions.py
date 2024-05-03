from rest_framework import permissions

from data.models import InstructionRole


class IsLoggedUser(permissions.BasePermission):
    message = "Vous devez être connecté et être l'utilisateur en question pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: User
        user = request.user
        return user.is_authenticated and user == obj


class CanAccessUserDeclatarions(permissions.BasePermission):
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


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return InstructionRole.objects.filter(user=request.user).exists()
