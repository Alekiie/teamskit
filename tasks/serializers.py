from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "id"]



class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.CharField(max_length=50)

    class Meta:
        model = Task
        fields = ["id","title", "description", "assignee_id", "due_date", "status"]
        read_only_fields=["id"]

    def validate_assignee_id(self, value):
        try:
            CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid assignee.")

        return value

    def create(self, validated_data):
        assignee_id = validated_data.pop("assignee_id")
        assignee = CustomUser.objects.get(id=assignee_id)
        

        task = Task.objects.create(
            assignee=assignee, creator=self.context["request"].user, **validated_data
        )

        return task

class TaskDetailSerializer(serializers.ModelSerializer):
    creator = UserSmallSerializer(read_only=True)
    assignee = UserSmallSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'creator', 'assignee', 'due_date', 'status',
            'created_on', 'last_updated_on'
        ]
        read_only_fields = ['id', 'created_on', 'last_updated_on']