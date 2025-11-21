from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer,CustomTokenObtainPairSerializer
from .permissions import IsAdmin,IsAdminOrManager
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

class CustomLoginView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer