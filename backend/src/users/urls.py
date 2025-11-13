from django.urls import path
from users.apis import LibraryUserListCreateAPIView

urlpatterns = [
    path("users/", LibraryUserListCreateAPIView.as_view(), name="user-list-create"),
]
