import hashlib
import hmac
import json
import os
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.views import IsAdminRole
from apps.orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Payment.objects.select_related('order').all().order_by('-created_at')
        return Payment.objects.select_related('order').filter(order__customer=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        idem = request.data.get('idempotency_key')
        order_id = request.data.get('order')
        existing = Payment.objects.filter(order_id=order_id, idempotency_key=idem).first()
        if existing:
            return Response(PaymentSerializer(existing).data, status=200)
        return super().create(request, *args, **kwargs)


class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        signature = request.headers.get('X-Signature', '')
        secret = os.getenv('PAYMENT_WEBHOOK_SECRET', 'webhook-secret').encode()
        payload = json.dumps(request.data, separators=(',', ':')).encode()
        expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return Response({'detail': 'Invalid signature'}, status=400)

        provider_payment_id = request.data.get('provider_payment_id')
        payment = Payment.objects.filter(provider_payment_id=provider_payment_id).select_related('order').first()
        if not payment:
            return Response({'detail': 'Unknown payment'}, status=404)

        payment.status = request.data.get('status', Payment.Status.FAILED)
        payment.save(update_fields=['status', 'updated_at'])
        order = payment.order
        order.status = Order.Status.CONFIRMED if payment.status == Payment.Status.SUCCESS else Order.Status.CANCELLED
        order.save(update_fields=['status', 'updated_at'])
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
