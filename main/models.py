from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=255,
                            choices=[('customer', 'customer'),
                                     ('staff', 'staff'),
                                     ('manager', 'manager')])
    phone = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = UserManager()

    def __str__(self):
        return f"<User: {self.first_name},{self.last_name}>"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=255)
    image = models.ImageField(default='/media/dragon.jpg', upload_to='users')
    is_mfa_enable = models.BooleanField(default=False)
    language_preference = models.CharField(max_length=255,
                                           choices=[('fr', 'french'),
                                                    ('en', 'english'),
                                                    ('gr', 'german'),
                                                    ('it', 'italian')],
                                           default='fr')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Profile: {self.user}>"


class Questionnaire(models.Model):
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaire')
    question = models.TextField(max_length=500)
    answer_choice = models.JSONField(default=dict)
    domain = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Questionnaire: {self.user}.{self.domain}>"


class UserQuestionnaireResponse(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaire_response')
    response = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Answer: {self.questionnaire}, {self.response}>"


