from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "page": {
                "paginator": {
                    "count": self.page.paginator.count,
                    "num_pages": self.page.paginator.num_pages,
                },
                "current": self.page.number,
                "has_next": self.page.has_next(),
                "has_previous": self.page.has_previous(),
            },
            "results": data
        })
