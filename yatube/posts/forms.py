from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        # на основе какой модели создаётся класс формы
        model = Post
        # укажем, какие поля будут в форме
        fields = ('text', 'group')
        labels = {
            'text': 'Текст',
            'group': 'Группа',
        }
        help_texts = {
            'text': 'fill in the text field',
            'group': 'select the group you need',
        }
