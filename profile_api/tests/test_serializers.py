from django.test import TestCase

from profile_api.models import Teacher, Category, CustomUser
from profile_api.serializers import TeacherProfileSerializer


class ProductSerializerTestCase(TestCase):

    def test_product_serializer(self):
        students = CustomUser.objects.create(email='deen345@gmail.com', first_name='Denik', last_name='jay', description='im student', city='New-York')
        category = Category.objects.create(title='English')
        teacher = Teacher.objects.create(email='denis123@gmail.com', first_name='Denis', last_name='Mel', description='Wow',
                                         city='Bishkek', experience='nuhh', specialization=category.title, students=students.id)
        srz = TeacherProfileSerializer(product, many=False)
        expected_data = {
            'id': teacher.id,
            'name': 'Наушники',
            'description': 'супер',
            'price': 20000,
        }
        self.assertEqual(srz.data, expected_data)

