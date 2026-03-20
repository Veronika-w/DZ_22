from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def  home(request):
    return render(request, 'home.html')


def  contacts(request):
    return render(request, 'contacts.html')


def product_list(request):
    catalogs = Product.objects.all()
    context = {"catalogs": catalogs}
    return render(request, 'product_list.html', context)


def get_objects_or_404(Product, pk):
    pass


def product_detail(request, pk):
    catalog = get_object_or_404(Product, pk=pk)
    context = {"catalog": catalog}
    return render(request, 'product_detail.html', context)