import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    home_page = serializers.URLField(required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'home_page', 'password','confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_confirm_password(self, confirm_password):
        """Validate that the passwords match."""
        password = self.initial_data.get('password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return confirm_password

    def validate_email(self, value):
        """Validate that the email address is unique."""
        existing_user = CustomUser.objects.filter(email=value).first()
        if existing_user:
            raise serializers.ValidationError('This email address is already in use.')
            # Проверка, соответствует ли имя пользователя указанному формату (буквы и цифры латинского алфавита)

    def validate_username(self, value):
        """Validate that the username is unique."""
        existing_user = CustomUser.objects.filter(username=value).first()
        if existing_user:
            raise serializers.ValidationError('This username is already in use.')
        if not re.match("^[a-zA-Z0-9]+$", value):
            raise serializers.ValidationError(
                'The username must contain only letters and numbers of the Latin alphabet.')

        return value



    def create(self, validated_data):
        """Create and return a new user instance."""
        confirm_password = validated_data.pop('confirm_password', None)
        password = validated_data.get('password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        user = CustomUser.objects.create_user(**validated_data)
        return user
