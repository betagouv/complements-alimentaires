from rest_framework import permissions


class IsDeclarant(permissions.BasePermission):
    message = "Vous devez être déclarant pour effectuer cette action"

    def has_permission(self, request, _):
        return request.user.is_authenticated and bool(request.user.role("declarant"))
