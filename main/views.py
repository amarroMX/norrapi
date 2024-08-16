from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Profile, Questionnaire
from .serializers import UserSerializer, ProfileSerializer, QuestionnaireSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing user model and get current logged in user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], url_path='me', renderer_classes=[renderers.JSONRenderer])
    def get_current_user(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing user's profile model."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing questionnaire model."""

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer



