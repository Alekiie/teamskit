from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializer import TaskSerializer
from accounts.permissions import IsAssigneeOrReadonly, IsAdminOrManager
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        user = self.request.user

        if self.action in ["create", "destroy"]:
            if user.role in ["Admin", "Manager"]:
                return [IsAuthenticated()]
            return [IsAdminOrManager()]

        if self.action in ["update", "partial_update"]:
            if user.role in ["Admin", "Manager"]:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsAssigneeOrReadonly()]

        if self.action in ["list", "retrieve", "recent", "assign_task"]:
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role in ["Admin", "Manager"]:
            return Task.objects.all()
        return Task.objects.filter(assignee=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    # recent activity
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def recent(self, request):
        """
        Returns the 6 most recently updated tasks
        """
        tasks = Task.objects.order_by("-last_updated_on")[:6]
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # assign task action - for admin/manager to assign tasks to team members
    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrManager])
    def assign_task(self, request, pk=None):
        """
        Assign a task to a team member
        Expected payload: {"assignee_id": user_id}
        """
        task = self.get_object()
        assignee_id = request.data.get("assignee_id")

        if not assignee_id:
            return Response(
                {"error": "assignee_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            assignee = CustomUser.objects.get(id=assignee_id)

            # check if the assignee is a team member (not admin/manager)
            if assignee.role in ["Admin", "Manager"]:
                return Response(
                    {"error": "Cannot assign tasks to other admins or managers"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        task.assignee = assignee
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAdminOrManager])
    def bulk_assign(self, request):
        """
        Bulk assign multiple tasks to a team member
        Expected payload: {"task_ids": [1, 2, 3], "assignee_id": user_id}
        """
        task_ids = request.data.get("task_ids", [])
        assignee_id = request.data.get("assignee_id")

        if not task_ids:
            return Response(
                {"error": "task_ids is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not assignee_id:
            return Response(
                {"error": "assignee_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            assignee = CustomUser.objects.get(id=assignee_id)

            #  Check if the assignee is a team member
            if assignee.role in ["Admin", "Manager"]:
                return Response(
                    {"error": "Cannot assign tasks to other admins or managers"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # get tasks that belong to the current user's scope
        tasks = self.get_queryset().filter(id__in=task_ids)

        if len(tasks) != len(task_ids):
            return Response(
                {
                    "error": "Some tasks were not found or you don't have permission to access them"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # update many tasks
        updated_count = tasks.update(assignee=assignee)

        return Response(
            {
                "message": f"Successfully assigned {updated_count} tasks to {assignee.username}",
                "assignee": assignee.username,
                "tasks_assigned": updated_count,
            }
        )
