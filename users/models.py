from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re


class CustomUser(AbstractUser):
    """Own user model to work with"""
    home_page = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        """Checking whether the user name corresponds to the specified format (Latin alphabet letters and digits)"""
        if not re.match("^[a-zA-Z0-9]+$", self.username):
            raise ValidationError('The username must contain only letters and numbers of the Latin alphabet.')

        super().save(*args, **kwargs)
