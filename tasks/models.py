from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


STATUS_OPTIONS = [
    ("Todo", "Todo"),
    ("In Progress", "In Progress"),
    ("Done", "Done"),
]


# Create your models here.
class Task(models.Model):

    # Task schema
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(
        User, related_name="created_tasks", on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    last_updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS_OPTIONS, default="Todo")

    def __str__(self):
        return self.title
