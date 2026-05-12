from django.db import models
from django.conf import settings


class Subject(models.Model):

    SUBJECT_TYPE_CHOICES = (
        ('compulsory', 'Compulsory'),
        ('optional_4th', 'Optional 4th'),
    )

    GROUP_CHOICES = (
        ('Science', 'Science'),
        ('Humanities', 'Humanities'),
        ('Business', 'Business'),
        ('All', 'All'),
    )

    name = models.CharField(max_length=100)

    code = models.CharField(max_length=20, unique=True)

    subject_type = models.CharField(
        max_length=20,
        choices=SUBJECT_TYPE_CHOICES
    )

    group = models.CharField(
        max_length=20,
        choices=GROUP_CHOICES,
        default='All'
    )

    class_levels = models.JSONField()

    has_practical = models.BooleanField(default=False)

    full_marks = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.name} ({self.code})"





class SubjectAssignment(models.Model):

    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    class_level = models.IntegerField()

    section = models.CharField(
        max_length=1,
        choices=SECTION_CHOICES
    )

    academic_year = models.IntegerField()

    def __str__(self):

        return (
            f"{self.teacher.username} - "
            f"{self.subject.name} - "
            f"{self.class_level}{self.section}"
        )
    




class Exam(models.Model):

    EXAM_TYPE_CHOICES = (
        ('class_test', 'Class Test'),
        ('half_yearly', 'Half Yearly'),
        ('annual', 'Annual'),
    )

    name = models.CharField(max_length=100)

    exam_type = models.CharField(
        max_length=20,
        choices=EXAM_TYPE_CHOICES
    )

    class_level = models.IntegerField()

    date = models.DateField()

    is_published = models.BooleanField(default=False)

    def __str__(self):

        return (
            f"{self.name} - "
            f"Class {self.class_level}"
        )
    

