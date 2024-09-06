from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet


class UserQuerySet(QuerySet):

    def is_active(self):
        return self.filter(is_active=True)

    def is_inactive(self):
        return self.filter(is_active=False)

    def is_customer(self):
        return self.filter(type__exact='customer')

    def is_staff(self):
        return self.filter(type__exact='staff')

    def is_manager(self):
        return self.filter(type__exact='manager')

    def has_subscription_plan(self):
        pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


