from django.db import models
from users.models import CustomUser
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone


def upload_comment_image(instance, filename):
    now = timezone.now()
    user_username = instance.user.username if instance.user else 'anonymous'
    return f'comment_images/{now.year}/{now.month}/{now.day}/{user_username}/{filename}'


class Comment(models.Model):
    """
       A model representing comments.

       Attributes:
           user (CustomUser): The user who posted the comment.
           text (TextField): The text content of the comment.
           created_at (DateTimeField): The date and time when the comment was created.
           parent_comment (Comment, optional): The parent comment to which this comment is a reply.
           replies (related_name): A reverse relation for accessing replies to a comment.
           image (ImageField, optional): An optional image attached to the comment.

       Meta:
           verbose_name (str): The singular name for the model in the Django admin.
           verbose_name_plural (str): The plural name for the model in the Django admin.
           indexes (list): A list of indexes to be created on the database table.
           ordering (list): The default sorting order for queries on the model.

       """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    image = models.ImageField(upload_to=upload_comment_image, blank=True, null=True)  # Add an image field

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return F"Comment_id: {self.id}"
