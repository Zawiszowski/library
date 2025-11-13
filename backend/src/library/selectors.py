from django.db.models import QuerySet

from library.models import Book


def library_list() -> QuerySet[Book]:
    queryset = Book.objects.select_related("author", "user")

    return queryset
