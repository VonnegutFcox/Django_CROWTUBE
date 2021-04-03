from django.test import TestCase

from yatube.posts.models import Post, Group


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            title='TEST',
            text='Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
                 'Тестовый текст,Тестовый текст,'
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PostModelTest.task
        field_verboses = {
            'text': 'Дайте короткое название задаче',
            'pub_date': 'date published',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта task записано значение поля task.title."""
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

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта task записано значение поля task.title."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))
