from rest_framework import permissions

from data.models import InstructionRole


class CanAccessUser(permissions.BasePermission):
    message = "Vous devez être connecté et être l'utilisateur en question pour effectuer cette action"

    def has_object_permission(self, request, view, obj):  # obj: User
        user = request.user
        is_instructor = IsInstructor().has_permission(request, view)
        if user.is_authenticated and user == obj:
            return True
        return request.method == "GET" and is_instructor


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


class CanAccessIndividualDeclaration(permissions.BasePermission):
    message = "Vous n'avez pas accès à cette déclaration"

    def has_object_permission(self, request, view, obj):  # obj: Declaration
        is_author = IsDeclarationAuthor().has_object_permission(request, view, obj)
        is_instructor = IsInstructor().has_permission(request, view)
        is_declarant = IsDeclarant().has_object_permission(request, view, obj)
        if request.method == "GET":
            return is_author or is_instructor

        return is_author and is_declarant
