from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(name='МФУ', description='компактный аппарат 3-в-1 или 4-в-1, '
                                                                             'объединяющий принтер, сканер, копир')

        products = [
            {'name': 'HP LaserJet Pro 4103dw', 'price': 35000.00, 'category': category},
            {'name': 'Kyocera ECOSYS M8124', 'price': 150000.00, 'category': category},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exist: {product.name}'))