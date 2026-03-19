from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions

from users.models import CustomUser
from users.serializers import RegisterUserSerializer

@extend_schema_view(
    post=extend_schema(auth=[])
)

class RegisterUser(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer