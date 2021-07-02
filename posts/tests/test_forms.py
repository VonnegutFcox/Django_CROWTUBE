# deals/tests/tests_form.py
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group, Comment

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='TestUser',
            password='testpassword123'
        )
        # Создадим запись в БД
        cls.group = Group.objects.create(
            title='Тест',
            slug='test-slug',
            description='Тестовый текст'
        )
        cls.post = Post.objects.create(
            pub_date='27 февраля 2021 г. 12:01',
            author=cls.user,
            text='Тестовый текст,Тестовый текст,',
            group=cls.group,
            image='posts/test-img.jpg'
        )
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'text': '+####TEST####+',
            'group': self.group.id,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:index'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись
        self.assertTrue(
            Post.objects.filter(
                text='+####TEST####+',
                group=self.group.id
            ).exists()
        )

    def test_create_post_with_image(self):
        """Валидная форма создает запись в Post с image"""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'text': 'post with image',
            'group': self.group.id,
            'image': SimpleUploadedFile('posts/test-img.jpg', b'')
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:index'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись
        self.assertTrue(
            Post.objects.filter(
                group=self.group.id
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'text': '+####TEST####+',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'username': self.user,
                        'post_id': self.post.id
                    }),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response,
                             reverse('posts:post', kwargs={
                                 'username': self.post.author.username,
                                 'post_id': self.post.id})
                             )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count)
        # Проверяем, что изменилась запись
        self.assertTrue(
            Post.objects.filter(
                text='+####TEST####+').exists()
        )

    def test_comment_page(self):
        """Только авторизированный пользователь может комментировать посты."""
        comments_count = Comment.objects.filter(author=self.user).count()
        form_data = {
            'text': '+####TEST####+',
            'author': self.user,
            'post': self.post.id
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment',
                    kwargs={'username': self.user,
                            'post_id': self.post.id}),
            data=form_data,
            follow=True
        )

        self.assertEqual(Comment.objects.filter(author=self.user).count(),
                         comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post.id,
                author=self.user,
                text='+####TEST####+'
            ).exists()
        )
