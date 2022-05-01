from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import EmailMessage, send_mail
from rest_framework.response import Response

from profile_api.models import Teacher, Reviews, CustomUser
from profile_api.serializers import TeacherProfileSerializer, ReviewSerialiazer, ClientLoginSerialiazer, \
    SendEmailSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id']
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'email']

    def perform_create(self, serializer):
        serializer.validated_data['email'] = self.request.user
        serializer.save()


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all().select_related('specialization').prefetch_related('students')
    serializer_class = TeacherProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id']
    search_fields = ['id', 'user']
    ordering_fields = ['id', 'specialization']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewSerialiazer
    queryset = Reviews.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClientLoginView(TokenObtainPairView):
    serializer_class = ClientLoginSerialiazer


class EmailMessageViewSet(APIView):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        srz = self.serializer_class(**request.data)
        try:
            teacher = Teacher.objects.get(pk=srz.data['teacher_id'])
        except Teacher.DoesNotExist:
            return Response({'message': 'Teacher not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        if self.serializer_class.teacher_email:
            send_mail(
                'Вами заинтерсовались',
                'Вами заинтересовался новый пользователь с сайта profile.kg',
                settings.EMAIL_HOST_USER,
                [self.serializer_class.teacher_email],
                fail_silently=True,
            )
