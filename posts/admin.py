from django.contrib import admin
from .models import Post, Group, Comment, Follow


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "text", "pub_date", "author", "group")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    # это свойство сработает для всех колонок:
    # где пусто - там будет эта строка


class GroupAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "title", "slug", "description")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("title",)
    # добавляем возможность фильтрации по дате
    list_filter = ("slug",)
    empty_value_display = "-пусто-"
    # это свойство сработает для всех колонок:
    # где пусто - там будет эта строка


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "post", "author", "text", "created")
    search_fields = ("post",)
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class FollowerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("user",)
    empty_value_display = "-пусто-"


# при регистрации модели Post источником
# конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowerAdmin)
