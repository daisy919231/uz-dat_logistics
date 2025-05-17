from django.shortcuts import render
from carrier.models import *
from shipper.models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.
def driver_accept_freight(driver, freight_id, truck, bid=False, bid_price=None):
    freight = Freight.objects.get(id=freight_id)
    truck = Truck.objects.get(driver=driver)

    if freight.status != Freight.StatusChoices.searching:
        raise ValueError("Freight already booked or unavailable")

    order = Order.objects.create(
        truck=truck,
        freight=freight,
        status=Order.StatusChoices.not_complete,
        bid=bid,
        bid_price=bid_price if bid else None,
        avto=truck.truck_number
    )

    freight.status = Freight.StatusChoices.booked
    freight.save()

    return order


@login_required
@require_POST
def driver_accept_freight_view(request):
    #Check if user is a driver
    if not hasattr(request.user, 'driver'):
        messages.error(request, "You are not registered as a driver.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    driver = request.user.driver
    freight_id = request.POST.get('freight_id')
    truck = Truck.objects.get(driver=driver)
    bid = request.POST.get('bid', False)
    bid_price = request.POST.get('bid_price')

    try:
        order = driver_accept_freight(driver, freight_id, truck, bid=bid, bid_price=bid_price)
        messages.success(request, "Freight accepted successfully!")
        return redirect('carrier:order-detail', order_id=order.id)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('shipper:freight-list')



def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, truck__driver__user=request.user)
    return render(request, 'carrier/order.html', {'order': order})


@login_required
def driver_orders(request):
    # Get orders for the current driver user
    orders = Order.objects.filter(truck__driver=request.user.driver)
    
    context = {
        'orders': orders,
        'title': 'My Orders'
    }
    return render(request, 'carrier/driver_orders.html', context)