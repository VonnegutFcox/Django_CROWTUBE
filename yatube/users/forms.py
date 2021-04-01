from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Contact


User = get_user_model()


class ContactForm(forms.ModelForm):
    name = forms.CharField(label="Введите имя")
    sender = forms.EmailField(label="Email для ответа")
    subject = forms.CharField(label="Тема сообщения", initial='Письмо администратору', max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(label="Отправить себе копию", required=False)

    class Meta:
        # на основе какой модели создаётся класс формы
        model = Contact
        # укажем, какие поля будут в форме
        fields = ('name', 'email', 'subject', 'body')


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("first_name", "last_name", "username", "email")
