import pytest
from django.urls import reverse_lazy, resolve
from tests.factories import LibraryFactory, AuthorFactory
from rest_framework import status


@pytest.mark.django_db()
class TestLibraryListAPI:
    viewname = "api:library:list"
    url = reverse_lazy(viewname)

    def test_reversed_url(self):
        assert self.url == "/api/library/books/"

    def test_resolved_view(self):
        resolved = resolve(self.url)
        assert resolved.view_name == self.viewname

    def test_response(self, annonymus_client):
        author = AuthorFactory()
        LibraryFactory(author=author)
        response = annonymus_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
