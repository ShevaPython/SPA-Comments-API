from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re


class CustomUser(AbstractUser):
    """Собственная модель пользователя для работы с ней"""
    home_page = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # Проверка, соответствует ли имя пользователя указанному формату (буквы и цифры латинского алфавита)
        if not re.match("^[a-zA-Z0-9]+$", self.username):
            raise ValidationError('Имя пользователя должно содержать только буквы и цифры латинского алфавита.')

        super().save(*args, **kwargs)
