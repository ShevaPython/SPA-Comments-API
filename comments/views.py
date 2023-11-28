from django.db.models import Exists, OuterRef
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentAllSerializer, CommentCreateSerializer, RootCommentSerializer, NestedCommentSerializer
from .service import PaginationComments


class CommentCreateView(generics.CreateAPIView):
    """
        A view for creating new comments.

        Fields:
        - queryset: A data set for extracting comments.
        - Serializer_class: Serializer for validating and processing comment data.

        Methods:
        - perform_create: Method to save the created comment.
        - post: Method to process HTTP POST request to create a new comment.

        When creating a comment, checks if the user is authenticated. If successful
        If successful, returns a success message and the data of the created comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:register')

        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            # Comment created successfully
            comment_data = response.data
            return Response({"message": "Comment created successfully", "comment": comment_data},
                            status=status.HTTP_201_CREATED)

        # If unable to create a comment
        return response


class CommentAllListView(generics.ListAPIView):
    """
        A view to retrieve a list of all root comments and their children.

        Fields:
        - queryset: A dataset to retrieve the root comments.
        - serializer_class: A serializer to convert the comment data into JSON format.
        - filter_backends: List of filters applied to the query.
        - ordering_fields: Fields by which to order the query results.

        Return values:
        - JSON representation of the list of root comments ordered by the specified fields.
    """
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentAllSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['user__username', 'user__email', 'created_at']


class RootCommentListView(generics.ListAPIView):
    """
        A view to retrieve a list of root comments.

        Fields:
        - serializer_class: Serializer to convert root comment data into JSON format.
        - filter_backends: List of filters applied to the request.
        - ordering_fields: Fields by which to order the query results.

        Methods:
        - get_queryset(): Returns a dataset containing root comments with no responses.

        Return values:
        - JSON representation of the list of root comments ordered by the specified fields.
    """
    serializer_class = RootCommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['user__username', 'user__email', 'created_at']
    pagination_class = PaginationComments

    def get_queryset(self):
        # Get the root comments IDs
        root_comment_ids = Comment.objects.filter(parent_comment__isnull=True).values_list('id', flat=True)

        # We get the very first comments we start replying to
        queryset = Comment.objects.filter(id__in=root_comment_ids).exclude(parent_comment__in=root_comment_ids)

        return queryset


class CommentDetailView(generics.RetrieveAPIView):
    """
        A view to get detailed information about the comment.

        Fields:
        - queryset: A dataset containing all comments.
        - Serializer_class: A serializer to convert the comment data into JSON format.
    """
    queryset = Comment.objects.all()
    serializer_class = NestedCommentSerializer
