from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    

class CommentPaginator(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 20
