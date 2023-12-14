from rest_framework import permissions


class IsInGroupBasePermission(permissions.BasePermission):
    group_name: str

    def has_permission(self, request, view):
        if request.user:
            if request.user.is_superuser:
                return True
            return request.user.groups.filter(name=self.group_name).exists()


class IsModerator(IsInGroupBasePermission):
    group_name = 'moderator'


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user == obj.owner or request.user.is_superuser)
