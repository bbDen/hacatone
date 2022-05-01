from datetime import timezone

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from profile_api.models import Teacher, Reviews, CustomUser, Student


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class ReviewSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('email', 'sent_at', 'name', 'message', 'parent', 'teacher')

        def create(self, validated_data):
            request = self.context.get('request')
            return Reviews.objects.create(
                email=request.user,
                sent_at=timezone.now(),
                **validated_data)


class ClientLoginSerialiazer(TokenObtainPairSerializer):
    """Даем клиенту токен"""
    def validate(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password', None)
        if not CustomUser.objects.filter(username=email).exists():
            raise serializers.ValidationError(('User not found'))
        user = CustomUser.objects.get(username=email)
        if user and user.is_active and user.check_password(password):
            self.refresh = self.get_token(user)
            validated_data['refresh'] = str(self.refresh)
            validated_data['access'] = str(self.refresh.access_token)
            return validated_data
        raise serializers.ValidationError('Email or password is incorrect')


class SendEmailSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()
    body = serializers.CharField(max_length=300)
    teacher_email = serializers.EmailField()
