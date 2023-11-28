from rest_framework import serializers

from users.models import CustomUser
from .models import Comment


class CustomUserCommentSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', ]


class CommentAllSerializer(serializers.ModelSerializer):
    """
        Serializer for the Comment model with additional information.

        Attributes:
        -----------
        model : Comment
            The comment model that this class serializes.

        fields : list
            List of fields of the Comment model that will be serialized.

        Methods:
        --------
        get_replies(self, obj)
            Method to get serialized responses to a comment.

        to_representation(self, instance)
            Overridden method to convert a Comment object into a dictionary.

    """
    replies = serializers.SerializerMethodField()
    user = CustomUserCommentSerializer
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

        # Let's make sure that created_at exists and is not a string
        if 'created_at' in representation and not isinstance(representation['created_at'], str):
            representation['created_at'] = representation['created_at'].strftime("%Y-%m-%d %H:%M")

        return representation


class RootCommentSerializer(serializers.ModelSerializer):
    """
        A serializer for the Comment model representing the main comment.

        Attributes:
        -----------
        model : Comment
            The comment model that this class serializes.

        fields : list
            List of fields of the Comment model that will be serialized.

    """
    user = CustomUserCommentSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'image', 'text', 'created_at']


class NestedCommentSerializer(serializers.ModelSerializer):
    """
        A serializer for the Comment model representing nested comments.

        Attributes:
        -----------
        model : Comment
            The comment model that this class serializes.

        fields : list
            List of fields of the Comment model that will be serialized.

         Methods:
        --------
        get_replies(self, obj)
        Method to get serialized responses to a comment.
        Gets and serializes responses to the given comment.

        Returns:
        -------
        list
            Serialized data for responses to the comment.



    """
    user = CustomUserCommentSerializer()
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
    """
        Serializer for creating comments.

        Fields:
        - text: The text of the comment.
        - image: The image attached to the comment.
        - parent_comment_id: ID of the parent comment (optional).

        Methods:
        - create: Method to create the comment. If `parent_comment_id` is specified, creates a comment within the
          specified parent comment. Otherwise creates the parent comment.
    """
    parent_comment_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['text', 'image', 'parent_comment_id']

    def create(self, validated_data):
        # Get the current user from the query
        user = self.context['request'].user
        # Extract parent comment ID from validated data
        parent_comment_id = validated_data.pop('parent_comment_id', None)

        if parent_comment_id:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            comment = Comment.objects.create(user=user, parent_comment=parent_comment, **validated_data)
        else:
            comment = Comment.objects.create(user=user, **validated_data)

        return comment
