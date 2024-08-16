from django.db.models import QuerySet
from django.db.models import Sum, Count
from django.db import models


class CourseQuerySet(QuerySet):

    def is_active(self):
        return self.filter(is_active=True)

    def by_category(self, category=None):
        return self.filter(category=category)

    def get_total_course_duration(self):
        total_course_duration = self.prefetch_related('chapters').aggregate(
            total_course_duration=Sum(
                Sum(
                    'chapters_modules__video__duration',
                    output_field=models.DecimalField(),
                ) + Sum(
                    'chapters_modules__quizzes__completed_in',
                    output_field=models.DecimalField(),
                ) + Sum(
                    'chapters_modules__resources__completed_in',
                    output_field=models.DecimalField(),
                )
            )
        ).get('total_course_duration') or 0

        return total_course_duration

    def get_total_course_completion(self, day=5):
        return self.get_total_course_duration() // 5

    def get_total_course_chapters(self):
        total_course_chapters = self.aggregate(
            total_course_modules=Count('chapters')
        ).get('total_course_chapters') or 0

        return total_course_chapters

    def get_total_course_module(self):
        pass
        total_course_modules = self.prefetch_related('chapters').aggregate(
            total_course_modules=Count('chapters_modules')
        ).get('total_course_modules') or 0

        return total_course_modules


class ChapterQuerySet(QuerySet):

    def get_total_duration(self):
        total_duration = self.prefetch_related('modules').aggregate(
            total_duration=Sum(
                Sum(
                    'modules__video__duration',
                    output_field=models.DecimalField()
                ) + Sum(
                    'modules__quizzes__completed_in',
                    output_field=models.DecimalField()
                ) + Sum(
                    'modules__resources__completed_in',
                    output_field=models.DecimalField()
                )
            )
        )['total_duration'] or 0

        return total_duration

    def get_total_completion_day(self):
        total_duration = self.get_total_duration()
        total_completion = round(total_duration // 5)
        return total_completion

    def get_total_modules_quizzes(self):
        total_quizzes = self.prefetch_related('modules').aggregate(
            total_modules_quizzes=Count('modules__quizzes')
        )
        return total_quizzes['total_modules_quizzes'] or 0

    def get_total_module_resources(self):
        total_resources = self.prefetch_related('modules').aggregate(
            total_resources=Count('modules__resources')
        )

        return total_resources['total_resources'] or 0


class ModuleQuerySet(QuerySet):

    def get_duration_minute(self):
        """total duration in minutes including video, quizz and reading"""

        video_duration = self.aggregate(
            total_video_duration=Sum('video__duration')
        )['total_video_duration'] or 0

        # Aggregate the total duration of all related quizzes
        quiz_duration = self.aggregate(
            total_quiz_duration=Sum('quizzes__completed_in')
        )['total_quiz_duration'] or 0

        # Aggregate the total duration of all related resources (reading)
        resource_duration = self.aggregate(
            total_resource_duration=Sum('resources__completed_in')
        )['total_resource_duration'] or 0

        # Calculate the total duration
        total_duration = video_duration + quiz_duration + resource_duration

        return total_duration

    def get_completion_time_day(self):
        total_duration = self.get_duration_minute()
        return total_duration // 2

    def get_total_quizzes(self):
        total_quizzes = self.aggregate(
            total_total_quizzes=Count('quizzes')
        )
        return total_quizzes['total_total_quizzes'] or 0

    def get_total_resources(self):
        total_resources = self.aggregate(
            total_total_resources=Count('resources')
        )

        return total_resources['total_resources'] or 0
