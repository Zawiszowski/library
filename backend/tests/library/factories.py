import factory
from datetime import datetime

from src.library.models import BookState


def random_datetime() -> datetime:
    return datetime.now()


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda x: f"{x:06d}")
    name = factory.Faker("first name")
    surename = factory.Faker("surename")


class AuthorFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(int)
    name = factory.Faker("first name")
    surename = factory.Faker("surename")


class LibraryFacroty(factory.django.DjangoModelFactory):
    id = factory.Sequence(int)
    library_code = factory.Sequence(lambda x: f"{x:06d}")
    title = factory.faker.Faker("sequence", nb_words=4)
    author = factory.SubFactory("tests.factories.AuthorFactory")
    user = factory.SubFactory("tests.factories.UserFactory")
    state = factory.Iterator(BookState.values)
    borrowed_since = factory.LazyFunction(random_datetime)
