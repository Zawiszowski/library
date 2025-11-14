from django.db import transaction
from django.utils import timezone

from library.models import Book, Author, BookState
from users.models import LibraryUser


def update_book_state(id: str, user_id: str | None = None) -> Book:
    with transaction.atomic():
        book = Book.objects.get(library_code=id)

        if user_id:
            user_id = LibraryUser.objects.get(id=user_id)
            book.user = user_id
            book.state = BookState.BORROWED
            book.borrowed_since = timezone.now()
            book.save(update_fields=["user", "state", "borrowed_since"])
        else:
            book.user = None
            book.state = BookState.FREE
            book.borrowed_since = None
            book.save(update_fields=["user", "state", "borrowed_since"])

        return book


def add_book(
    *,
    library_code: str,
    title: str,
    author_name: str,
    author_surname: str,
    user: str | None = None,
) -> Book:
    """Create book with author."""
    with transaction.atomic():
        author, _ = Author.objects.get_or_create(
            name=author_name, surename=author_surname
        )

        book = Book.objects.create(
            library_code=library_code,
            title=title,
            author=author,
        )

        if user:
            book = update_book_state(book.library_code, user)

    return book
