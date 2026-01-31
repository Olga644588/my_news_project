import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='articles/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False, verbose_name='Основной раздел')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scopes', to='news.article')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scopes', to='news.tag')),
            ],
            options={
                'verbose_name': 'Связь статьи с тегом',
                'verbose_name_plural': 'Связи статей с тегами',
                'unique_together': {('article', 'tag')},
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='articles', through='news.Scope', to='news.tag', verbose_name='Теги статьи'),
        ),
    ]
