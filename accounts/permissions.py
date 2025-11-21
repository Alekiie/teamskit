from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Only the admin has the permission to perform this action."

    def has_permission(self, request, view):
        return request.user.role == "Admin"


class IsManager(BasePermission):
    message="Only the manager has the permission to perform this action."
    def has_permission(self, request, view):
        return request.user.role in ["Manager"]


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["Admin", "Manager"]


class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["Member"]


class IsAssigneeOrReadonly(BasePermission):
    """

    Members can only update the tasks that have been assigned to them.
    Managers or Admins can update tasks.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role in ["Admin", "Manager"]:
            return True
        return obj.assignee == request.user
