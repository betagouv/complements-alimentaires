from rest_framework import permissions


class IsLoggedUser(permissions.BasePermission):
    message = "Vous devez être connecté et être l'utilisateur en question pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj


class IsDeclarantOfThisCompany(permissions.BasePermission):
    message = "Vous devez être déclarant pour effectuer cette action"

    def has_permission(self, request, _):
        return request.user.is_authenticated and bool(request.user.role("declarant"))

    def has_object_permission(self, request, view, obj):
        user = request.user
        return self.has_permission(request, view) and obj.company.declarants.filter(user=user).exists()


class IsSupervisorOfThisCompany(permissions.BasePermission):
    message = "Vous devez être gestionnaire de cette entreprise pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and obj.supervisors.filter(user=user).exists()


class IsDeclarationAuthor(permissions.BasePermission):
    message = "Vous devez être l'auteur de cette déclaration pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
