from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'created_at', 'parent_comment']
    search_fields = ['user__username', 'text']
    list_filter = ['created_at', 'parent_comment']
