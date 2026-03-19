import pytest

from rest_framework.test import APIClient

from store.models import Author, Book, Order
from users.models import CustomUser


@pytest.mark.django_db
def test_order():
    client = APIClient()
    user = CustomUser.objects.create_superuser(username='test_username', password='test_password')
    client.force_authenticate(user=user)

    author = Author.objects.create(
        name='test_author',
        bio='test_bio',
        birth_date="1950-01-01"
    )

    book = Book.objects.create(
        price=10.13,
        stock_quantity=10,
        title="test_book",
        description="test_description",
        author=author,
    )

    data = {
        'book': book.id,
        'quantity': 1,
    }

    response = client.post('/orders/', data)

    assert response.status_code == 201

    book.refresh_from_db()
    assert book.stock_quantity == 9

@pytest.mark.django_db
def test_stock_quantity():
    client = APIClient()
    user = CustomUser.objects.create_superuser(username='test_username', password='test_password')
    client.force_authenticate(user=user)

    author = Author.objects.create(
        name='test_author',
        bio='test_bio',
        birth_date="1950-01-01"
    )

    book = Book.objects.create(
        price=10.13,
        stock_quantity=4,
        title="test_book",
        description="test_description",
        author=author,
    )

    data = {
        'book': book.id,
        'quantity': 5,
    }

    response = client.post('/orders/', data)

    assert response.status_code == 400

    book.refresh_from_db()
    assert book.stock_quantity == 4

@pytest.mark.django_db
def test_anonymous_order():
    client = APIClient()

    author = Author.objects.create(
        name='test_author',
        bio='test_bio',
        birth_date="1950-01-01"
    )

    book = Book.objects.create(
        price=10.13,
        stock_quantity=4,
        title="test_book",
        description="test_description",
        author=author,
    )

    data = {
        'book': book.id,
        'quantity': 1,
    }

    response = client.post('/orders/', data)

    assert response.status_code == 401

@pytest.mark.django_db
def test_order_total_sum():
    client = APIClient()
    user = CustomUser.objects.create_superuser(username='test_username', password='test_password')
    client.force_authenticate(user=user)

    author = Author.objects.create(
        name='test_author',
        bio='test_bio',
        birth_date="1950-01-01"
    )

    book = Book.objects.create(
        price=10.00,
        stock_quantity=10,
        title="test_book",
        description="test_description",
        author=author,
    )

    data = {
        'book': book.id,
        'quantity': 2,
    }

    response = client.post('/orders/', data)

    assert response.status_code == 201

    order_id = response.data['id']
    order = Order.objects.get(pk=order_id)

    assert order.total_price == 20.00

@pytest.mark.django_db
def test_total_price_calculation():
    client = APIClient()
    user = CustomUser.objects.create_superuser(username='test_username', password='test_password')
    client.force_authenticate(user=user)

    author = Author.objects.create(
        name='test_author',
        bio='test_bio',
        birth_date="1950-01-01"
    )

    book = Book.objects.create(
        price=10.00,
        stock_quantity=10,
        title="test_book",
        description="test_description",
        author=author,
    )

    data = {
        'book': book.id,
        'quantity': -1,
    }

    response = client.post('/orders/', data)

    assert response.status_code == 400