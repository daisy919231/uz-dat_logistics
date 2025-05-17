from django.urls import path
from carrier.views import order_detail, driver_accept_freight_view, driver_orders, export_orders_to_excel, AllOrdersView
app_name='carrier'

urlpatterns = [
    path('orders/<int:order_id>/', order_detail, name='order-detail'),
    path('driver/accept/', driver_accept_freight_view, name='accept-freight'),
    path('driver/orders/', driver_orders, name='driver-orders'),
    path('export-orders/', export_orders_to_excel, name='export-orders'),
    path('all_orders/', AllOrdersView.as_view(), name='all-orders')
]