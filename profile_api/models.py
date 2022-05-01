from django.contrib.auth.models import AbstractUser
from django.db import models

from profile_api.managers import CommentManager


class AbstractTimeStampModel(models.Model):
    """Дата создания"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    """Категория"""
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Gender(models.Model):
    """Пол"""
    gender = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.gender


class CustomUser(AbstractUser):
    """Юзер"""
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Student(CustomUser):
    """Студент"""
    profession = models.CharField(max_length=100)


class Teacher(AbstractTimeStampModel, CustomUser):
    """Учитель"""
    experience = models.CharField(max_length=100)
    specialization = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='categories')
    students = models.ManyToManyField(to=CustomUser, related_name='students')


class Reviews(models.Model):
    """Отзывы"""
    email = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='users')
    sent_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField("Имя", max_length=100)
    message = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    teacher = models.ForeignKey(to=Teacher, verbose_name="отзывы", on_delete=models.CASCADE)

    objects = CommentManager()

    def __str__(self):
        return f"{self.name} - {self.teacher}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
