from django.urls import path, include

from library.apis import (
    LibraryListAPI,
    RemoveBookViewSet,
    BookCreateAPIView,
    BookUpdateStateAPIView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"book-delete", RemoveBookViewSet, basename="book-delete")

urlpatterns = [
    path("books/", LibraryListAPI.as_view(), name="list"),
    path("books/create", BookCreateAPIView.as_view(), name="book-create"),
    path("books/update", BookUpdateStateAPIView.as_view(), name="book-update"),
    path("", include(router.urls)),
]
