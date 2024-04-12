from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsLoggedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return isinstance(obj, get_user_model()) and request.user.is_authenticated and request.user == obj


class IsDeclarant(permissions.BasePermission):
    message = "Vous devez être déclarant pour effectuer cette action"

    def has_permission(self, request, _):
        return request.user.is_authenticated and bool(request.user.role("declarant"))


class IsDeclarationAuthor(permissions.BasePermission):
    message = "Vous devez être l'auteur de cette déclaration pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
