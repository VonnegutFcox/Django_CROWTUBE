from django import forms
from django.forms import Textarea

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        # на основе какой модели создаётся класс формы
        model = Post
        # укажем, какие поля будут в форме
        fields = ['group', 'text', 'image']
        labels = {
            'text': 'Текст',
            'group': 'Группа',
            'image': 'Изображение'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Текст',
        }
        widgets = {'text': Textarea()}
