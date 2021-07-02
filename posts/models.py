from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        help_text='Заголовок вашей группы',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Адрес для страницы',
        help_text='Адрес страницы с постами группы',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание вашей группы',
    )

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='fill in the text field')
    pub_date = models.DateTimeField(
        verbose_name='date published',
        help_text='дата публикации поста',
        auto_now_add=True)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='posts',
                               help_text='автор данного поста')
    group = models.ForeignKey(Group,
                              verbose_name='Группа',
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              help_text='select the group you need',
                              blank=True, null=True)
    image = models.ImageField(upload_to='posts/',
                              blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             verbose_name='Post',
                             on_delete=models.CASCADE,
                             related_name='comments',
                             help_text='ссылка на пост, к которому оставлен комментарий',
                             blank=True, null=False)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               help_text='ссылка на автора комментария')
    text = models.TextField(
        verbose_name='Text',
        help_text='текст комментария')
    created = models.DateTimeField(
        verbose_name='date published',
        help_text='дата публикации комментария',
        auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Follow(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='User',
                             on_delete=models.CASCADE, related_name='follower',
                             help_text='ссылка на объект пользователя,'
                                       ' который подписывается')
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='following',
                               help_text='ссылка на объект пользователя,'
                                         ' на которого подписываются')

    class Meta:
        db_table = 'posts_follow'
        constraints = [
            models.UniqueConstraint(fields=['author'],
                                    condition=Q(status='DRAFT'),
                                    name='unique_author_follower')
        ]