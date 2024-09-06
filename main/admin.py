from PIL.Image import module
from django.contrib import admin
from . import  models

admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Questionnaire)
admin.site.register(models.UserQuestionnaireResponse)