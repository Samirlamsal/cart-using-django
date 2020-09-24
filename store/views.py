from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json

def store(request):
    products = Product.objects.all()
    return render(request, 'store/store.html',{'products':products})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_total_items':0}
    return render(request, 'store/cart.html', {'items':items, 'order':order})


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_total_items':0}
    return render(request, 'store/checkout.html', {'items':items, 'order':order})



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action=='add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)
