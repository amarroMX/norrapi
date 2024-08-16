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


