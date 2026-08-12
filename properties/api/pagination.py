from rest_framework.pagination import PageNumberPagination


class PropertySubmissionPagination(PageNumberPagination):
    """
    Pagination for property submissions.

    Default:
        10 submissions per page.

    Maximum:
        50 submissions per page.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_data(self, serializer_data):
        """
        Return pagination metadata in the application's
        standard API response format.
        """

        return {
            "results": serializer_data,
            "pagination": {
                "count": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
        }
