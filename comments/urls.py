# ваше_приложение/urls.py
from django.urls import path
from .views import CommentCreateView, CommentListView, RootCommentListView, CommentDetailView

app_name = 'comments'

urlpatterns = [
    path('comment/create/', CommentCreateView.as_view(), name='comment-create'),
    path('list_all_info/', CommentListView.as_view(), name='list_all_info'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('', RootCommentListView.as_view(), name='root-list')
]
