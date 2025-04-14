
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import default_storage
from PIL import Image
import os

class Board(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"/{self.abbreviation}/ - {self.name}"

class Thread(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} (/{self.board.abbreviation}/)"

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    is_op = models.BooleanField(default=False)
    author = models.CharField(max_length=50, default="Аноним")
    email = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"Post #{self.id} by {self.author}"

    def save(self, *args, **kwargs):
        if not self.thread and not self.is_op:
            raise ValueError("Only OP posts can be without thread")
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Сохраняем сначала модель, чтобы получить ID
        super().save(*args, **kwargs)

        # Если есть изображение - обрабатываем его
        if self.image:
            try:
                img_path = self.image.path
                if default_storage.exists(img_path):
                    with Image.open(img_path) as img:
                        # Уменьшаем изображение, если оно слишком большое
                        if img.width > 2000 or img.height > 2000:
                            img.thumbnail((2000, 2000))
                            img.save(img_path)
            except Exception as e:
                # В случае ошибки просто продолжаем
                print(f"Error processing image: {e}")