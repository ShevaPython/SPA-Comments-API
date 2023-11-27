# serializers.py
from rest_framework import serializers

from users.models import CustomUser
from .models import Comment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', ]


class CommentAllSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'image', 'text', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentAllSerializer(replies, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Убедимся, что created_at существует и не является строкой
        if 'created_at' in representation and not isinstance(representation['created_at'], str):
            representation['created_at'] = representation['created_at'].strftime("%Y-%m-%d %H:%M")

        return representation


class RootCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'image', 'text', 'created_at']


class NestedCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'image', 'text', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = NestedCommentSerializer(replies, many=True)
        return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):
    parent_comment_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['text', 'image', 'parent_comment_id']

    def create(self, validated_data):
        user = self.context['request'].user
        parent_comment_id = validated_data.pop('parent_comment_id', None)

        if parent_comment_id:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            comment = Comment.objects.create(user=user, parent_comment=parent_comment, **validated_data)
        else:
            comment = Comment.objects.create(user=user, **validated_data)

        return comment
