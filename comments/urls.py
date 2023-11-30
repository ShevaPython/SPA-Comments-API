from django.urls import path
from .views import CommentCreateView, CommentAllListView, RootCommentListView, CommentDetailView

app_name = 'comments'

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='comment-create'),
    path('list_all_info/', CommentAllListView.as_view(), name='list_all_info'),
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('', RootCommentListView.as_view(), name='root-list'),

]
