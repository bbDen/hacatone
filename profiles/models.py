from django.db import models
from django.contrib.auth.models import User

from profiles.managers import CommentManager


class AbstractTimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Gender(models.Model):
    gender = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.gender


class Teacher(AbstractTimeStampModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='media/scherbakov.jpg')
    description = models.TextField(blank=True, null=True)
    cat = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories')
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    gender = models.ForeignKey(to=Gender, on_delete=models.SET_NULL, null=True, blank=True, related_name='genders')
    city = models.CharField(max_length=100)
    students = models.ManyToManyField(User)

    def __str__(self):
        return self.specialization


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField(User)
    sent_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField("Имя", max_length=100)
    message = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    nukura = models.ForeignKey(Teacher, verbose_name="отзывы", on_delete=models.CASCADE)

    objects = CommentManager()

    def __str__(self):
        return f"{self.name} - {self.nukura}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
