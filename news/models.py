from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='articles/', verbose_name='Изображение')

    tags = models.ManyToManyField(
        Tag,
        through='Scope',
        related_name='articles',  
        verbose_name='Теги статьи'
    )

    def __str__(self):
        return self.title
class Scope(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='scopes'  
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='scopes'
    )
    is_main = models.BooleanField(default=False, verbose_name='Основной раздел')

    def __str__(self):
        return f"{self.article.title} → {self.tag.name} (основной: {self.is_main})"

    class Meta:
        unique_together = ('article', 'tag')
