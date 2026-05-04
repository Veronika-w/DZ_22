from django.forms import ModelForm
from django.core.exceptions import ValidationError

from catalog.models import Product

SPAM = ['казино', 'биржа', 'обман', 'криптовалюта', 'дешево', 'полиция', 'крипта', 'бесплатно', 'радар']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ("views_counter",)


    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
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
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        name_lower = name.lower()
        forbidden_words = []
        for word in SPAM:
            if word.lower() in name_lower:
                forbidden_words.append(word)
        if forbidden_words:
            raise ValidationError(
                f'Запрещенные слова "{", ".join(forbidden_words)}" нельзя использовать в названии продукта')
        return cleaned_data


    def clean_description(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        description_lower = description.lower()
        forbidden_words = []
        for word in SPAM:
            if word.lower() in description_lower:
                forbidden_words.append(word)
        if forbidden_words:
            raise ValidationError(
                f'Запрещенные слова "{", ".join(forbidden_words)}" нельзя использовать в описании продукта')
        return cleaned_data