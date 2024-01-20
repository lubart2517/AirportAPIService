from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )


class IsAllowedToCreateOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method == "POST":
            return bool(request.user)
        else:
            return bool(
                request.user
                and (obj.user == request.user or request.user.is_staff)
            )
