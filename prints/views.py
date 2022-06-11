from django.shortcuts import render
from .models import Category, Product, ProductVariant


def show_all_prints(request):
    template = "prints/show_all_prints.html"
    context = {}

    return render(request, template, context)