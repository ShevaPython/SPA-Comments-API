from .models import Comment
from rest_framework.pagination import PageNumberPagination


class PaginationComments(PageNumberPagination):
    page_size = 25
