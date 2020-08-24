from django.shortcuts import render
from .models import Item

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "item_list.html", context)


def checkout(request):
    return render(request, "checkout.html")


def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home.html", context)
