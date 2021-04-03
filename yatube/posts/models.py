from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Адрес для страницы',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group,
                              verbose_name='Группа',
                              on_delete=models.SET_NULL,
                              related_name="posts",
                              blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']

    @classmethod
    def __str__(cls):
        return cls.text[:15]
