from django.db import models
from shortuuid.django_fields import ShortUUIDField


class LibraryUser(models.Model):
    id = ShortUUIDField(
        length=6, alphabet="0123456789", primary_key=True, max_length=6, editable=False
    )
    name = models.CharField(max_length=65)
    surename = models.CharField(max_length=65)

    class Meta:
        db_table = "library_user"
