from django.urls import path, include

urlpatterns = [
    path("library/", include(("library.urls", "library"))),
    path("users/", include(("users.urls", "users"))),
]
