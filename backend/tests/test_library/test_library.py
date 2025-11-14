import pytest
from tests.factories import LibraryFactory
from library.selectors import library_list


@pytest.mark.django_db(transaction=True)
def test_selector_book_list(db):
    LibraryFactory.create_batch(10)
    result = library_list()
    assert len(result) == 10
