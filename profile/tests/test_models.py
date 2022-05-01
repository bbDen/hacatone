from django.test import TestCase

from profile_api.models import Category


class TestTeacherCategoryModel(TestCase):

    def test_create_article(self):
        category = Category.objects.create(title='первая тестовая категория')
        self.assertEqual(category.title, 'первая тестовая категория')

    def test_create_article_count(self):
        Category.objects.create(title='тестовая категория')
        category_count = Category.objects.count()
        self.assertEqual(category_count, 1)