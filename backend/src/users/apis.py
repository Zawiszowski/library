from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema
from users.models import LibraryUser
from rest_framework import serializers


class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = ["id", "name", "surename"]
        read_only_fields = ["id"]


class LibraryUserListCreateAPIView(ListCreateAPIView):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer

    @extend_schema(
        summary="List users",
        description="Return users list.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create user",
        description="Create user with 6-digit id.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
