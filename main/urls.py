from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'form', views.QuestionnaireViewSet)

urlpatterns = router.get_urls()