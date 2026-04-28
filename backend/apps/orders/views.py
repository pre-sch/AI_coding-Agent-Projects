from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.accounts.models import User
from apps.catalog.views import IsAdminRole
from .models import Cart, Order, Shipment
from .serializers import CartSerializer, CheckoutSerializer, OrderSerializer, ShipmentSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).prefetch_related('items')
        guest_id = self.request.query_params.get('guest_id')
        return Cart.objects.filter(guest_id=guest_id).prefetch_related('items')

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = Order.objects.prefetch_related('items').order_by('-created_at')
        if self.request.user.role == User.Role.ADMIN:
            return qs
        return qs.filter(customer=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in Order.Status.values:
            return Response({'detail': 'Invalid status'}, status=400)
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        return Response(OrderSerializer(order).data)


class ShipmentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Shipment.objects.select_related('order')
    serializer_class = ShipmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]
