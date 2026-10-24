from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(
        upload_to="catalog/image", blank=True, null=True, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publication_sign = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_counter = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)

    def __str__(self):
        return f"{self.title} {self.content}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["title"]