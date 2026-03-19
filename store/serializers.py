from rest_framework import serializers
from store.models import Book, Author, Order

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)
    stock_quantity = serializers.IntegerField(min_value=0, default=0)

    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=0, default=0)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)
    class Meta:
        model = Order
        fields = ['id', 'user', 'book', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'user', 'total_price', 'created_at']

    def validate(self, attrs):
        book = attrs['book']
        quantity = attrs['quantity']

        if book.stock_quantity < quantity:
            raise serializers.ValidationError('Requested quantity exceeds available stock.')

        return attrs
