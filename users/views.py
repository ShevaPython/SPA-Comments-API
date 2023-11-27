# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from users.serializers import CustomUserSerializer


class RegistrationView(generics.CreateAPIView):
    """View for user registration."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        """Handle user registration."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Add user activation before saving
        user = serializer.save(is_active=True)

        # You can send an activation letter here if needed

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)

