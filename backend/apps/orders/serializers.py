from django.db import transaction
from rest_framework import serializers
from apps.catalog.models import Product
from apps.inventory.models import InventoryTransaction
from .models import Cart, CartItem, Order, OrderItem, Shipment


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'guest_id', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)
        for item in items_data:
            CartItem.objects.create(cart=cart, **item)
        return cart


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer', 'total_amount', 'status']


class CheckoutSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    shipping_name = serializers.CharField()
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField()
    shipping_state = serializers.CharField()
    shipping_postal_code = serializers.CharField()
    shipping_country = serializers.CharField()
    idempotency_key = serializers.CharField(required=False, allow_blank=True)

    @transaction.atomic
    def create(self, validated_data):
        cart = Cart.objects.select_for_update().prefetch_related('items__product').get(id=validated_data['cart_id'])
        customer = self.context['request'].user
        idem = validated_data.get('idempotency_key', '')
        if idem:
            existing = Order.objects.filter(customer=customer, idempotency_key=idem).first()
            if existing:
                return existing

        order = Order.objects.create(
            customer=customer,
            shipping_name=validated_data['shipping_name'],
            shipping_address=validated_data['shipping_address'],
            shipping_city=validated_data['shipping_city'],
            shipping_state=validated_data['shipping_state'],
            shipping_postal_code=validated_data['shipping_postal_code'],
            shipping_country=validated_data['shipping_country'],
            idempotency_key=idem,
        )

        total = 0
        for item in cart.items.all():
            product = Product.objects.select_for_update().get(pk=item.product_id)
            if product.stock < item.quantity:
                raise serializers.ValidationError(f'Insufficient stock for {product.name}')
            product.stock -= item.quantity
            product.save(update_fields=['stock', 'updated_at'])
            InventoryTransaction.objects.create(
                product=product,
                transaction_type=InventoryTransaction.TransactionType.SALE,
                quantity_change=-item.quantity,
                reason=f'Order #{order.id}',
            )
            OrderItem.objects.create(order=order, product=product, quantity=item.quantity, unit_price=product.price)
            total += product.price * item.quantity

        order.total_amount = total
        order.save(update_fields=['total_amount', 'updated_at'])
        cart.items.all().delete()
        return order


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
