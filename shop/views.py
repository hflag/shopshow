from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from .models import Category, Product


class ProductsView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        return render(request, 'shop/product/list.html', {'category': category,
                                                          'categories': categories,
                                                          'products': products})


class ProductView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)
        return render(request, 'shop/product/detail.html', {'product': product})
