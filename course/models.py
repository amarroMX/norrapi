from django.db import models
from main.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Category: {self.name}>'""


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses',
                                   limit_choices_to={'is_staff': True, 'is_manager': True})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Course: {self.title}, {self.category}, {self.instructor}>"


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    order = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=100, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = (('course', 'title'), ('course', 'order'),)

    def __str__(self):
        return f"<chapter: {self.title}, {self.course}, {self.order}>"


class Module(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    video = models.OneToOneField('Video', on_delete=models.CASCADE, related_name='module')
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = (('chapter', 'video'), ('chapter', 'order'))

    def __str__(self):
        return f"<module: {self.title}, {self.chapter}, {self.order}>"


class Quizz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    answers = models.JSONField()
    order = models.PositiveSmallIntegerField()
    completed_in = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

# sample answer {
#     "A": {
#         "text": "Choice A description",
#         "is_correct": False
#     },
#     "B": {
#         "text": "Choice B description",
#         "is_correct": True
#     },
#     "C": {
#         "text": "Choice C description",
#         "is_correct": False
#     },
#     "D": {
#         "text": "Choice D description",
#         "is_correct": False
#     }
# }


class Resources(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to='resources')
    type = models.CharField(max_length=50)
    completed_in = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)


class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to='videos')
    duration = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    name = models.CharField(max_length=100, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    features = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubscriptionDuration(models.Model):
    DURATION_UNIT_CHOICES = [
        ('month', 'Month'),
        ('year', 'Year'),
    ]

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='durations')
    duration_value = models.PositiveIntegerField()
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"<SubscriptionDuration {self.plan.name}, {self.duration_value}>"

    def get_total_duration(self):
        """
        Calculate the total duration in days based on the duration value and unit.
        """
        if self.duration_unit == 'month':
            return self.duration_value * 30
        elif self.duration_unit == 'year':
            return self.duration_value * 365

    def get_price_per_day(self):
        """
        Calculate the price per day.
        """
        total_days = self.get_total_duration()
        return self.price // total_days
