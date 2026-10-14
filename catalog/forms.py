from django.forms import ModelForm
from django.core.exceptions import ValidationError

from catalog.models import Product

SPAM = ['казино', 'биржа', 'обман', 'криптовалюта', 'дешево', 'полиция', 'крипта', 'бесплатно', 'радар']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ("views_counter",
                   "owner",
                   "unpublish_product",)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите наименование товара'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Загрузите изображение'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите категорию'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену'})

    def clean_price(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной.')
        return price


    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            forbidden = [w for w in SPAM if w.lower() in name.lower()]
            if forbidden:
                raise ValidationError(
                    f'Запрещенные слова "{", ".join(forbidden)}" нельзя использовать в названии продукта'
                )
        return name


    def clean_description(self):
        name = self.cleaned_data.get("description")
        if name:
            forbidden = [w for w in SPAM if w.lower() in name.lower()]
            if forbidden:
                raise ValidationError(
                    f'Запрещенные слова "{", ".join(forbidden)}" нельзя использовать в описании продукта'
                )
        return name


class ProductModeratorForm(ModelForm):
    class Meta:
        model = Product
        fields = ("unpublish_product",)
