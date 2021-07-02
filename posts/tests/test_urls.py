# posts/tests/tests_url.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='TestUser',
            password='testpassword123')
        cls.group = Group.objects.create(
            title='Тест',
            slug='test-slug',
            description='Тестовый текст'
        )
        cls.post = Post.objects.create(
            pub_date='27 февраля 2021 г. 12:01',
            author=cls.user,
            text='Тестовый текст,Тестовый текст,',
            group=cls.group
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

        self.templates_url_names = {
            'index.html': (reverse('posts:index'), 200),
            'posts/new.html': (reverse('posts:new_post'), 302),
            'group.html': (reverse('posts:show_group',
                                   kwargs={'slug': 'test-slug'}), 200),
            'profile.html': (reverse('posts:profile',
                                     kwargs={'username': self.user}), 200),
            'new.html': (reverse('posts:post_edit',
                                 kwargs={'username': self.user,
                                         'post_id': self.post.id}), 302),
            'post.html': (reverse('posts:post',
                                  kwargs={'username': self.user,
                                          'post_id': self.post.id}), 200),
        }

    def test_pages_code(self):
        """Проверка дотсупа к страницам анонимных пользователей."""
        for reverse_name, code in self.templates_url_names.values():
            with self.subTest():
                response = self.guest_client.get(reverse_name)
                self.assertEqual(response.status_code, code)

    def test_postpage_edit_url_exists_at_desired_location_authorized(self):
        """Страница /<str:username>/<int:post_id>/edit/
         доступна автору поста."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': self.user,
                            'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_postpage_edit_url_redirect_authorized(self):
        """Страница /<str:username>/<int:post_id>/edit/
        перенаправляет не автора поста."""
        authorized_test_client = Client()
        authorized_test_client.force_login(
            User.objects.create_user(
                username='TestWrong',
                password='wrong'))
        response = authorized_test_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': self.user,
                            'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_new_url_exists_at_desired_location_authorized(self):
        """Страница /new/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get(reverse('posts:new_post'))
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, (reverse_name, _) in self.templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_postpage_edit_url_redirect_anonymous_on_postpage(self):
        """
        Страница по адресу /<str:username>/<int:post_id>/edit/
        перенаправит анонимного пользователя на страницу поста.
        """
        response = self.guest_client.get(reverse('posts:post_edit',
                                                 kwargs={
                                                     'username': self.user,
                                                     'post_id': self.post.id}),
                                         follow=True)
        # не знаю как поменять на reverse()
        self.assertRedirects(response, '/auth/login/?next=/TestUser/1/edit/')

    def test_404(self):
        response = self.guest_client.get('/test404/')
        self.assertEqual(response.status_code, 404)

    def test_follow_unfollow_user_page(self):
        """Авторизованный пользователь может подписываться
         на других пользователей и удалять их из подписок."""
        user1 = User.objects.create_user(
            username='User',
            password='123')
        url_names = {
            'follow': reverse('posts:profile_follow', kwargs={'username': user1}),
            'unfollow': reverse('posts:profile_unfollow', kwargs={'username': user1})
        }
        for url in url_names.items():
            with self.subTest():
                response = self.authorized_client.get(url[1])
                anonymous = self.guest_client.get(url[1])
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(anonymous, f'/auth/login/?next=/{user1}/{url[0]}/')
