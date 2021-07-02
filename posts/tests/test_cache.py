from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group
from django.core.cache import cache

User = get_user_model()


class CacheTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='TestUser',
            password='testpassword123'
        )
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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_index_page(self):
        response_before = self.authorized_client.get(reverse('posts:index'))

        self.new_post = Post.objects.create(
            text='Text for test',
            author=self.user,
            group=self.group,
        )
        response_after = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(
            response_before.content,
            response_after.content
        )
        cache.clear()
        response_after_cache_clear = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(
            response_before.content,
            response_after_cache_clear.content
        )

