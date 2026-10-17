from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from catalog.services import get_products_from_cache


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет прав отменить публикацию продукта.')

        product.unpublish_product = False
        product.save()

        return redirect('catalog:product_detail', pk=pk)


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_edit_product'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_delete_product'):
            return ProductModeratorForm
        raise PermissionDenied


# 1. ГЛОБАЛЬНЫЙ ПАТЧ: Отключаем RESP3/HELLO и уведомления об обслуживании для старого Redis на Windows
from redis.connection import Connection

# Отключаем проверку уведомлений об обслуживании, которая вызывает RedisError
Connection._configure_maintenance_notifications = lambda *args, **kwargs: None

# Перехватываем инициализацию соединения и принудительно задаем протокол RESP2
original_init = Connection.__init__
def patched_init(self, *args, **kwargs):
    kwargs['protocol'] = 2  # Блокирует команду HELLO
    original_init(self, *args, **kwargs)
Connection.__init__ = patched_init