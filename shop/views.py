from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from .models import Category, Product
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class ProductsView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        # 商品分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 每页设定为8件商品
        p = Paginator(products, 8, request=request)

        perpage_products = p.page(page)

        return render(request, 'shop/product/list.html', {'category': category,
                                                          'categories': categories,
                                                          'products': perpage_products})


class ProductView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)
        return render(request, 'shop/product/detail.html', {'product': product})
