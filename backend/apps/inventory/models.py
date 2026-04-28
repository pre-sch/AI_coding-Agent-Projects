from django.db import models
from apps.catalog.models import Product


class InventoryTransaction(models.Model):
    class TransactionType(models.TextChoices):
        SALE = 'sale', 'Sale'
        RESTOCK = 'restock', 'Restock'
        ADJUSTMENT = 'adjustment', 'Adjustment'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_transactions')
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity_change = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['product', 'created_at'])]
