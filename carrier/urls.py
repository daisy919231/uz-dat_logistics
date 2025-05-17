from django.urls import path
from carrier.views import order_detail, driver_accept_freight_view, driver_orders
app_name='carrier'

urlpatterns = [
    path('orders/<int:order_id>/', order_detail, name='order-detail'),
    path('driver/accept/', driver_accept_freight_view, name='accept-freight'),
    path('driver/orders/', driver_orders, name='driver-orders'),
]