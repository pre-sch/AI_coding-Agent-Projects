from celery import shared_task
from apps.catalog.models import Product


@shared_task
def low_stock_alert_task(threshold=5):
    return list(Product.objects.filter(stock__lte=threshold).values('id', 'name', 'stock'))
