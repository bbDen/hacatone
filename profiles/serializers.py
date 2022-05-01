from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import Teacher


class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
