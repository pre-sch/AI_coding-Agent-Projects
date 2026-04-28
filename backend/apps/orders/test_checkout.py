import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.catalog.models import Category, Product
from apps.orders.models import Cart, CartItem, Order


@pytest.mark.django_db
def test_checkout_creates_order_and_decrements_stock():
    user = get_user_model().objects.create_user(username='c1', password='secret123')
    category = Category.objects.create(name='Cat', slug='cat')
    product = Product.objects.create(category=category, name='P1', sku='SKU1', price=10, stock=5, description='d')
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product, quantity=2)

    client = APIClient()
    client.force_authenticate(user=user)
    res = client.post('/api/orders/checkout/', {
        'cart_id': cart.id,
        'shipping_name': 'John',
        'shipping_address': 'Street 1',
        'shipping_city': 'Austin',
        'shipping_state': 'TX',
        'shipping_postal_code': '78701',
        'shipping_country': 'US'
    }, format='json')

    assert res.status_code == 201
    assert Order.objects.count() == 1
    product.refresh_from_db()
    assert product.stock == 3
