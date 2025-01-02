# accounts/views.py
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from .serializers import PasswordResetSerializer
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PasswordResetSerializer
from rest_framework.response import Response

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Se ha enviado un email para restablecer la contraseña.'})


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Se ha enviado un email para restablecer la contraseña.'})

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'La contraseña ha sido restablecida con éxito.'})