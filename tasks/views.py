from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializer import TaskSerializer
from accounts.permissions import IsAssigneeOrReadonly, IsAdmin, IsManager, IsMember,IsAdminOrManager


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        user = self.request.user
        
        if self.action == "create" or self.action == "destroy":
            if user.role in ["Admin","Manager"]:
                return [IsAuthenticated()]
            return [IsAdminOrManager()]
        if self.action in ["update", "partial_update"]:
            if user.role in ["Admin", "Manager"]:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsAssigneeOrReadonly()]

        if self.action == "list" or self.action == "retrieve":
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Admin" or user.role == "Manager":
            return Task.objects.all()

        return Task.objects.filter(assignee=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
