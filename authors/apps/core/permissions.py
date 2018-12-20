from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = "Read only. You are not allowed to edit or delete"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to all
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to owner
        return obj.author == request.user

