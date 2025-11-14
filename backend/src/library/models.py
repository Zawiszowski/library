from django.db import models
from django.db.models.enums import TextChoices
from shortuuid.django_fields import ShortUUIDField

from users.models import LibraryUser


class BookState(TextChoices):
    FREE = "FREE", "Free"
    BORROWED = "BORROWED", "Borrowed"


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=65)
    surename = models.CharField(max_length=65)

    class Meta:
        db_table = "author"
        constraints = [
            models.UniqueConstraint(fields=["name", "surename"], name="full_name")
        ]


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    library_code = ShortUUIDField(
        length=6, alphabet="0123456789", unique=True, max_length=6, editable=True
    )  # TODO: validate in serializer
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        related_name="author_books",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        LibraryUser,
        related_name="user_books",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    state = models.CharField(choices=BookState.choices, default=BookState.FREE)
    borrowed_since = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "book"
