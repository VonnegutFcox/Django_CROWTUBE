# Generated by Django 3.1.7 on 2021-04-22 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='текст комментария', verbose_name='Text')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='дата публикации комментария', verbose_name='date published')),
                ('author', models.ForeignKey(help_text='ссылка на автора комментария', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(blank=True, help_text='ссылка на пост, к которому оставлен комментарий', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='Post')),
            ],
        ),
    ]
