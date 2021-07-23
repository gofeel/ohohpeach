import uuid

from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order, Product
from django.conf import settings


def index(request):
    return render(request, 'order/index.html')


def add_order(request):
    if settings.ORDER_CLOSE:
        return render(request, 'order/closed.html')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order:read-order-hid', hid=str(order.hid))
    else:
        form = OrderForm(initial={'product': Product.objects.first()})

    return render(request, 'order/add.html', {"form": form})


def read_order_hid(request, hid):
    try:
        order = Order.objects.get_with_hid(hid=hid)
        return render(request, 'order/read.html', {"order": order})
    except Order.DoesNotExist:
        return redirect('order:index')


@login_required
def browse_order(request):
    objects = Order.objects.order_by("shipping_id", "id").filter(shipping_id__gt=0).filter(shipping_id__lt=900)
    start = request.GET.get('start', None)
    if start:
        end = request.GET.get('end', None)
        start = int(start) - 1
        end = int(end)
        orders = objects[start:end]
    else:
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(objects, 10)
        orders = p.get_page(page)

    return render(request, 'order/browse.html', {"items": orders})


@login_required
def filter_order(request):
    orders = Order.objects.filter(shipping_id=0).order_by("id")
    return render(request, 'order/filter.html', {"items": orders})


@login_required
def send_order(_, order_id):
    order = Order.objects.get(id=order_id)
    a = Order.objects.filter(shipping_id__lt=900).order_by("-shipping_id").first()
    order.shipping_id = a.shipping_id + 1
    order.save()
    return redirect('order:filter')
