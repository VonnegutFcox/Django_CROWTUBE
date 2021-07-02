from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AboutURLTests(TestCase):
    """Проверка URL адресов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.template_names_urls = {
            'about/author.html': 'about:author',
            'about/tech.html': 'about:tech'
        }

    def test_about_page_accessible(self):
        """Проверка дотсупа к страницам не авторизованых пользователей."""
        for url_name in self.template_names_urls.values():
            with self.subTest():
                response = self.guest_client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """для отображения страниц /about/author/ и /about/tech/
        применяются ожидаемые view-функции и шаблоны"""
        for template, url in self.template_names_urls.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse(url))
                self.assertTemplateUsed(response, template)
