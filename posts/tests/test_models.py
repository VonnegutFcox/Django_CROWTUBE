# posts/tests/tests_models.py
from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post, Group


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username='TestUser',
            password='testpassword123'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,',
            author=user
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'date published',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'fill in the text field',
            'pub_date': 'дата публикации поста',
            'author': 'автор данного поста',
            'group': 'select the group you need',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта post
        записано значение поля post.text[:15]."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='TEST',
            slug='test',
            description='Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес для страницы',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_help_texts = {
            'title': 'Заголовок вашей группы',
            'slug': 'Адрес страницы с постами группы',
            'description': 'Описание вашей группы',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта group
        записано значение поля group.title."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))
