from rest_framework import permissions


class IsLoggedUser(permissions.BasePermission):
    message = "Vous devez être connecté et être l'utilisateur en question pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj


class IsDeclarant(permissions.BasePermission):
    message = "Vous devez être déclarant pour effectuer cette action"

    def has_permission(self, request, _):
        return request.user.is_authenticated and bool(request.user.role("declarant"))
