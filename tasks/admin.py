from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=['title','description','creator','assignee','created_on','due_date','last_updated_on','status']
    list_filter=['status','assignee']
    search_fields=['title']