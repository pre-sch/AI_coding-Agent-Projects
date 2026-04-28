import csv
from datetime import datetime
from django.db.models import Count, Sum
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.views import IsAdminRole
from apps.orders.models import Order, OrderItem


class AnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request):
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')
        orders = Order.objects.all()
        if start:
            orders = orders.filter(created_at__date__gte=datetime.strptime(start, '%Y-%m-%d').date())
        if end:
            orders = orders.filter(created_at__date__lte=datetime.strptime(end, '%Y-%m-%d').date())

        metrics = {
            'orders_count': orders.count(),
            'revenue': orders.aggregate(revenue=Sum('total_amount'))['revenue'] or 0,
            'daily_sales': list(
                orders.values('created_at__date').annotate(total=Sum('total_amount')).order_by('created_at__date')
            ),
            'top_products': list(
                OrderItem.objects.filter(order__in=orders)
                .values('product__name')
                .annotate(quantity=Sum('quantity'), order_count=Count('order', distinct=True))
                .order_by('-quantity')[:10]
            ),
        }

        if request.query_params.get('format') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="analytics.csv"'
            writer = csv.writer(response)
            writer.writerow(['metric', 'value'])
            writer.writerow(['orders_count', metrics['orders_count']])
            writer.writerow(['revenue', metrics['revenue']])
            return response
        return Response(metrics)
