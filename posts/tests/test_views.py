from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
import datetime
from posts.models import Post, Group, Comment

User = get_user_model()


class YatubePagesTests(TestCase):
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
            author=cls.user,
            text='Тестовый текст,Тестовый текст!',
            group=cls.group,
            image='posts/test-img.jpg'
        )

    def setUp(self):
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names = {
            'index.html': reverse('posts:index'),
            'posts/new.html': reverse('posts:new_post'),
            'group.html': (
                reverse('posts:show_group', kwargs={'slug': 'test-slug'})
            ),
        }
        # Проверяем, что при обращении к name
        # вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTrue(len(response.context.get('page').object_list) <= 10)
        post_object = response.context.get('page').object_list[0]
        post_details = {
            datetime.datetime.now().date(): post_object.pub_date.date(),
            'TestUser': post_object.author.username,
            'Тестовый текст,Тестовый текст!': post_object.text,
            'Тест': post_object.group.title
        }
        for detail, test_post in post_details.items():
            with self.subTest(detail=detail):
                self.assertEqual(detail, test_post)

    def test_index_show_image_correct_context(self):
        """шаблон index.html сформирован с правильным контекстом (image)"""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTrue(len(response.context.get('page').object_list) <= 10)
        post_object = response.context.get('page').object_list[0]
        post_image = post_object.image.name
        self.assertEqual(post_image, Post.objects.last().image)

    def test_profile_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        post_object = response.context.get('page').object_list[0]
        post_details = {
            datetime.datetime.now().date(): post_object.pub_date.date(),
            'TestUser': post_object.author.username,
            'Тестовый текст,Тестовый текст!': post_object.text,
            'Тест': post_object.group.title
        }
        for detail, test_post in post_details.items():
            with self.subTest(detail=detail):
                self.assertEqual(detail, test_post)

    def test_profile_show_image_correct_context(self):
        """шаблон profile сформирован с правильным контекстом (image)"""
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        post_object = response.context.get('page').object_list[0]
        post_image = post_object.image.name
        self.assertEqual(post_image, Post.objects.last().image)

    def test_post_correct_context(self):
        """Шаблон отдельного post сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:post', kwargs={
                'username': self.post.author.username,
                'post_id': self.post.id})
        )
        post_object = response.context.get('post')
        post_details = {
            datetime.datetime.now().date(): post_object.pub_date.date(),
            'TestUser': post_object.author.username,
            'Тестовый текст,Тестовый текст!': post_object.text,
            'Тест': post_object.group.title,
            '1': str(post_object.id),
        }
        for detail, test_post in post_details.items():
            with self.subTest(detail=detail):
                self.assertEqual(detail, test_post)

    def test_post_show_image_correct_context(self):
        """шаблон post.html сформирован с правильным контекстом (image)"""
        response = self.authorized_client.get(
            reverse("posts:post", kwargs={
                "username": self.post.author.username,
                "post_id": self.post.id}))
        post_object = response.context.get('post')
        post_image = post_object.image.name
        self.assertEqual(post_image, Post.objects.last().image)

    def test_groups_correct_context(self):
        """Шаблон show_group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:show_group', kwargs={'slug': 'test-slug'}))
        post_object = response.context.get('page').object_list[0]
        post_details = {
            datetime.datetime.now().date(): post_object.pub_date.date(),
            'TestUser': post_object.author.username,
            'Тестовый текст,Тестовый текст!': post_object.text,
            'Тест': post_object.group.title
        }
        for detail, test_post in post_details.items():
            with self.subTest(detail=detail):
                self.assertEqual(detail, test_post)

    def test_groups_show_image_correct_context(self):
        """шаблон groups сформирован с правильным контекстом (image)"""
        response = self.authorized_client.get(reverse(
            'posts:show_group', kwargs={'slug': 'test-slug'}))
        post_object = response.context.get('page').object_list[0]
        post_image = post_object.image.name
        self.assertEqual(post_image, Post.objects.last().image)

    def test_new_post_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_correct_context(self):
        """Шаблон /<username>/<post_id>/edit/
         сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={
                        'username': self.user, 'post_id': 1
                    })
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_new_post_desired_page(self):
        """если при создании поста указать группу,
         то этот пост появляется:
         * на главной странице сайта
         * на странице выбранной группы"""
        url_names = (
            reverse('posts:show_group',
                    kwargs={'slug': 'test-slug'}),
            reverse('posts:index')
        )
        for url in url_names:
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(len(response.context.get('page')), 1)

    def test_new_post_not_at_wrong_page(self):
        """пост не попал в группу,
        для которой не был предназначен"""
        response = self.authorized_client.get(reverse(
            'posts:show_group', kwargs={'slug': 'wrong-test-slug'}))
        self.assertFalse(response.context.get('page'))

    def test_new_follow_post_desired_page(self):
        """Новая запись пользователя появляется в ленте тех,
         кто на него подписан и не появляется в ленте тех,
          кто не подписан на него."""
        new_user = User.objects.create_user(
                username='User',
                password='123'
            )
        new_user_post = Post.objects.create(
            author=new_user,
            text='***********',
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertEqual(len(response.context.get('page')), 0)
        response = self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={'username': new_user}))
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertEqual(len(response.context.get('page')), 1)
