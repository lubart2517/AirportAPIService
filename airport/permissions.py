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


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(
             request.user and obj.user == request.user
        )


class IsAllowedToCreateOrAdmin(BasePermission):

    def has_permission(self, request, view):
        safe_methods_with_create = ('GET', 'HEAD', 'OPTIONS', 'CREATE')
        return bool(
            (
                    request.method in safe_methods_with_create
                    and request.user
                    and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
