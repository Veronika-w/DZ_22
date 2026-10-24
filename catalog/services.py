from django.core.cache import cache

from .models import Product,Category
from config.settings import CACHE_ENABLE


def get_products_from_cache():
    """Получает данные по продуктам их кэша, если кэш пуст, получает данные из бд."""
    if not CACHE_ENABLE:
        return Product.objects.all()
    key = 'products_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


CATEGORY_CACHE_TIMEOUT = 60


class ProductService:

    @staticmethod
    def get_products_category(category_id: int):
        cache_key = f"category_{category_id}"
        products = cache.get(cache_key)

        if products is None:
            products = list(
                Product.objects.filter(category_id=category_id)
            )
            cache.set(
                cache_key,
                products,
                timeout=CATEGORY_CACHE_TIMEOUT,
            )

        return products