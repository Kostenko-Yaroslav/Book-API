from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from store.permissions import CustomerAccessPermission
from store.serializers import AuthorSerializer, BookSerializer, OrderSerializer
from store.models import Author, Book, Order

@extend_schema_view(
    list=extend_schema(auth=[]),
    retrieve=extend_schema(auth=[])
)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [CustomerAccessPermission]
    http_method_names = ['get', 'post']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    pagination_class = LimitOffsetPagination

@extend_schema_view(
    list=extend_schema(auth=[]),
    retrieve=extend_schema(auth=[])
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [CustomerAccessPermission]
    http_method_names = ['post', 'get', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author']
    pagination_class = LimitOffsetPagination

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'book').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ['post']

    def perform_create(self, serializer):
        with transaction.atomic():
            book_obj = serializer.validated_data['book']
            quantity = serializer.validated_data['quantity']

            book = Book.objects.select_for_update().get(pk=book_obj.pk)

            if book.stock_quantity < quantity:
                raise ValidationError("Requested quantity exceeds available stock.")

            book.stock_quantity -= quantity
            book.save()

            total_price = book.price * quantity

            serializer.save(
                user=self.request.user, 
                total_price=total_price, 
                book=book
            )

