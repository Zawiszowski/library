from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    extend_schema_serializer,
    OpenApiResponse,
)
from rest_framework import serializers, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    GenericAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from library.models import Book, Author
from library.services import add_book, update_book_state
from library.selectors import library_list
from users.models import LibraryUser


@extend_schema_serializer(component_name="LibraryUserSerializer")
class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = "__all__"


@extend_schema_serializer(component_name="AuthorSerializer")
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "surename"]


@extend_schema_serializer(component_name="LibraryList")
class LibrarySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    user = LibraryUserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


@extend_schema_serializer(component_name="CreateBookSerializer")
class BookCreateSerializer(serializers.Serializer):
    library_code = serializers.RegexField(
        regex=r"^\d{6}$",
        max_length=6,
        min_length=6,
        help_text="6-digit code",
    )
    title = serializers.CharField(max_length=60)
    author_name = serializers.CharField(max_length=60)
    author_surname = serializers.CharField(max_length=60)
    user = serializers.RegexField(
        regex=r"^\d{6}$",
        required=False,
        allow_null=True,
        help_text="6-digit user id",
    )

    def create(self, validated_data):
        return add_book(**validated_data)


@extend_schema_serializer(component_name="UpdateBookSerializer")
class BookUpdateStateSerializer(serializers.Serializer):
    library_code = serializers.RegexField(
        regex=r"^\d{6}$",
        max_length=6,
        min_length=6,
        required=True,
        help_text="6-digit library id",
    )

    user_id = serializers.RegexField(
        regex=r"^\d{6}$",
        max_length=6,
        min_length=6,
        required=True,
        help_text="6-digit user id",
    )


@extend_schema_serializer(component_name="DeleteBookSerializer")
class BookDeleteSerializer(serializers.Serializer):
    library_code = serializers.RegexField(
        regex=r"^\d{6}$",
        max_length=6,
        min_length=6,
        help_text="6-digit code",
    )


@extend_schema_view()
class LibraryListAPI(ListAPIView):
    serializer_class = LibrarySerializer
    pagination_class = LimitOffsetPagination
    ordering = ["-id"]

    def get_queryset(self):
        return library_list()


class BookCreateAPIView(CreateAPIView):
    serializer_class = BookCreateSerializer

    @extend_schema(
        summary="Create book with author",
        description="Create book with author.",
        request=BookCreateSerializer,
        responses={201: LibrarySerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.save()

        output = LibrarySerializer(book)
        return Response(output.data, status=status.HTTP_201_CREATED)


class BookUpdateStateAPIView(GenericAPIView):
    serializer_class = BookUpdateStateSerializer

    @extend_schema(
        summary="Update book state",
        description="Set state of book on borrowed or free.",
        request=BookUpdateStateSerializer,
        responses={
            200: LibrarySerializer,
            404: OpenApiResponse(description="Book or user not found"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        library_code = serializer.validated_data["library_code"]
        user_id = serializer.validated_data.get("user_id")

        try:
            Book.objects.get(library_code=library_code)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=404)

        if user_id is not None:
            try:
                LibraryUser.objects.get(pk=user_id)
            except LibraryUser.DoesNotExist:
                return Response({"detail": "User not found."}, status=404)

        book = update_book_state(library_code, user_id)

        return Response(LibrarySerializer(book).data, status=200)


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete book by library_code",
        description="Delete book by 6-digit library_code",
        responses={204: None, 404: None},
    ),
)
class RemoveBookViewSet(DestroyModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = LibrarySerializer
    lookup_field = "library_code"
    lookup_value_regex = r"\d{6}"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        code = self.kwargs[self.lookup_field]
        try:
            return queryset.get(**{self.lookup_field: code})
        except Book.DoesNotExist:
            raise NotFound("Book with this library_code does not exist.")
