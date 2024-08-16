from rest_framework import serializers
from .models import User, Profile, Questionnaire


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class QuestionnaireSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        questionnaire = Questionnaire.objects.create(
            user=self.re,
            questionnaire=validated_data['questionnaire'],
            answer=validated_data['answer']
        )
        return questionnaire

    class Meta:
        model = Questionnaire
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
