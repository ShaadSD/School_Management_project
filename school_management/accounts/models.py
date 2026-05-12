from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username



class StudentProfile(models.Model):
    GROUP_CHOICES = (
        ('Science', 'Science'),
        ('Humanities', 'Humanities'),
        ('Business', 'Business'),
    )

    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.IntegerField()
    class_level = models.IntegerField()
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)

    group = models.CharField(
        max_length=20,
        choices=GROUP_CHOICES,
        null=True,
        blank=True
    )

    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    address = models.TextField()

    def __str__(self):
        return self.user.username





class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    employee_id = models.CharField(max_length=50)

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username





class ParentStudentLink(models.Model):
    RELATION_CHOICES = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Guardian', 'Guardian'),
    )

    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='parent_links'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_links'
    )

    access_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATION_CHOICES
    )

    def __str__(self):
        return f"{self.parent.username} -> {self.student.username}"