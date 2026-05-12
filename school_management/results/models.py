from django.db import models
from django.conf import settings

from academics.models import Exam, Subject


class StudentMark(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    marks_written = models.FloatField(default=0)

    marks_mcq = models.FloatField(default=0)

    marks_practical = models.FloatField(
        null=True,
        blank=True
    )

    total_marks = models.FloatField(default=0)

    letter_grade = models.CharField(
        max_length=5,
        blank=True
    )

    grade_point = models.FloatField(default=0)

    is_absent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        unique_together = ['student', 'exam', 'subject']

    def __str__(self):

        return (
            f"{self.student.username} - "
            f"{self.subject.name} - "
            f"{self.exam.name}"
        )

    def calculate_total_marks(self):

        practical = self.marks_practical or 0

        return (
            self.marks_written +
            self.marks_mcq +
            practical
        )

    def calculate_grade(self, total):

        if total >= 80:
            return 'A+', 5.0

        elif total >= 70:
            return 'A', 4.0

        elif total >= 60:
            return 'A-', 3.5

        elif total >= 50:
            return 'B', 3.0

        elif total >= 40:
            return 'C', 2.0

        elif total >= 33:
            return 'D', 1.0

        else:
            return 'F', 0.0

    def save(self, *args, **kwargs):

        if self.is_absent:

            self.total_marks = 0
            self.letter_grade = 'F'
            self.grade_point = 0.0

        else:

            total = self.calculate_total_marks()

            self.total_marks = total

            grade, gp = self.calculate_grade(total)

            self.letter_grade = grade
            self.grade_point = gp

        super().save(*args, **kwargs)





class StudentResult(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    gpa = models.FloatField(default=0)

    total_marks = models.FloatField(default=0)

    class_position = models.IntegerField(
        null=True,
        blank=True
    )

    is_passed = models.BooleanField(default=True)

    total_grade_points = models.FloatField(default=0)

    number_of_subjects = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        unique_together = ['student', 'exam']

    def __str__(self):

        return (
            f"{self.student.username} - "
            f"{self.exam.name} - GPA {self.gpa}"
        )