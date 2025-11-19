from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username","id"]


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSmallSerializer(read_only=True)
    assignee = UserSmallSerializer(read_only=True)
    
    assignee_id=serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="assignee",
        write_only=True,
    )
    
    creator_id=serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="creator",
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "due_date",
            "last_updated_on",
            "creator",
            "assignee",
            "creator_id",
            "assignee_id",
            "status",
        ]
