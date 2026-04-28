from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from apps.accounts.views import RegisterView, UserView
from apps.catalog.views import CategoryViewSet, ProductViewSet
from apps.orders.views import CartViewSet, OrderViewSet, ShipmentViewSet
from apps.payments.views import PaymentViewSet, PaymentWebhookView
from apps.analytics_app.views import AnalyticsView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'shipments', ShipmentViewSet, basename='shipments')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/me/', UserView.as_view()),
    path('api/auth/token/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/analytics/', AnalyticsView.as_view()),
    path('api/payments/webhook/', PaymentWebhookView.as_view()),
    path('api/', include(router.urls)),
]
