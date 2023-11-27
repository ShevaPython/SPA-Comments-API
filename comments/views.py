from django.db.models import Exists, OuterRef
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentAllSerializer, CommentCreateSerializer, RootCommentSerializer, NestedCommentSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:register')

        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            # Комментарий успешно создан
            comment_data = response.data
            return Response({"message": "Comment created successfully", "comment": comment_data},
                            status=status.HTTP_201_CREATED)

        # Если не удалось создать комментарий
        return response


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentAllSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['user__username', 'user__email', 'created_at']


class RootCommentListView(generics.ListAPIView):
    serializer_class = RootCommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['user__username', 'user__email', 'created_at']

    def get_queryset(self):
        # Получаем идентификаторы корневых комментариев
        root_comment_ids = Comment.objects.filter(parent_comment__isnull=True).values_list('id', flat=True)

        # Получаем самые первые комментарии, на которые начали отвечать
        queryset = Comment.objects.filter(id__in=root_comment_ids).exclude(parent_comment__in=root_comment_ids)

        return queryset

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = NestedCommentSerializer
