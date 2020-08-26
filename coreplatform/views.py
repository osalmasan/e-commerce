from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "item_list.html", context)


def checkout(request):
    return render(request, "checkout.html")


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity has been updated")

        else:
            order.items.add(order_item)
            messages.info(request, "Item has been added to cart.")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item has been added to cart.")

    return redirect("coreplatform:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Item has been removed from cart.")
            return redirect("coreplatform:product", slug=slug)

        else:
            # add a message saying the user doesnt have an order
            messages.info(request, "You do not have an active order.")
            return redirect("coreplatform:product", slug=slug)

    else:
        # add a message saying the user doesnt have an order
        messages.info(request, "Item has been added to cart.")
        return- redirect("coreplatform:product", slug=slug)

    return redirect("coreplatform:product", slug=slug)


class HomeView(ListView):
    model = Item
    template_name = 'home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
