from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["id","username","email","role","is_active","is_staff"]
        read_only_fields = ["is_staff"]