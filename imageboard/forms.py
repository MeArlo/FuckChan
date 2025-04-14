from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from django.conf import settings
import os

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'email', 'subject', 'message', 'image']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Аноним'}),
            'email': forms.TextInput(attrs={'placeholder': 'sage'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Тема'}),
            'message': forms.Textarea(attrs={'placeholder': 'Сообщение'}),
        }

        def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                # Проверка размера файла
                if image.size > settings.MAX_IMAGE_SIZE:
                    raise ValidationError(
                        f"Файл слишком большой. Максимальный размер: {settings.MAX_IMAGE_SIZE // (1024 * 1024)}MB")

                # Проверка расширения файла
                ext = os.path.splitext(image.name)[1].lower()
                if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
                    raise ValidationError(
                        f"Неподдерживаемый формат изображения. Разрешены: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}")

            return image