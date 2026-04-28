from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id):
    return f'email queued for order {order_id}'


@shared_task
def send_shipping_update(order_id):
    return f'shipping update queued for order {order_id}'
