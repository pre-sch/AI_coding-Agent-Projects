import hashlib
import hmac
import json
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.orders.models import Order
from apps.payments.models import Payment


@pytest.mark.django_db
def test_payment_webhook_updates_order_status(settings):
    settings.PAYMENT_WEBHOOK_SECRET = 'webhook-secret'
    user = get_user_model().objects.create_user(username='u1', password='secret123')
    order = Order.objects.create(
        customer=user,
        shipping_name='N',
        shipping_address='A',
        shipping_city='C',
        shipping_state='S',
        shipping_postal_code='P',
        shipping_country='US',
        total_amount=20,
    )
    Payment.objects.create(order=order, provider_payment_id='pay_1', amount=20, idempotency_key='abc')

    payload = {'provider_payment_id': 'pay_1', 'status': 'success'}
    raw = json.dumps(payload, separators=(',', ':')).encode()
    signature = hmac.new(b'webhook-secret', raw, hashlib.sha256).hexdigest()

    client = APIClient()
    res = client.post('/api/payments/webhook/', payload, format='json', HTTP_X_SIGNATURE=signature)
    assert res.status_code == 200
    order.refresh_from_db()
    assert order.status == 'confirmed'
