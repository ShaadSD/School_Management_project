from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

from accounts.models import (
    StudentProfile,
    TeacherProfile,
    ParentStudentLink
)

from academics.models import (
    Subject,
    SubjectAssignment,
    Exam
)

from results.models import (
    StudentMark
)

from results.services import (
    calculate_student_result,
    generate_merit_list
)

from attendance.models import Attendance

from datetime import date, timedelta

import random

User = get_user_model()


class Command(BaseCommand):

    help = 'Seed school management data'

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS('Seeding started...')
        )

        # -----------------------------
        # ADMIN
        # -----------------------------

        admin, created = User.objects.get_or_create(
            username='admin'
        )

        admin.email = 'admin@school.com'
        admin.role = 'admin'
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('admin123')
        admin.save()

        # -----------------------------
        # TEACHERS
        # -----------------------------

        teachers = []

        for i in range(1, 4):

            teacher, created = User.objects.get_or_create(
                username=f'teacher{i}'
            )

            teacher.email = f'teacher{i}@school.com'
            teacher.role = 'teacher'
            teacher.set_password('teacher123')
            teacher.save()

            TeacherProfile.objects.get_or_create(
                user=teacher,
                defaults={
                    'employee_id': f'EMP00{i}',
                    'department': 'Science',
                    'designation': 'Teacher'
                }
            )

            teachers.append(teacher)

        # -----------------------------
        # PARENT
        # -----------------------------

        parent, created = User.objects.get_or_create(
            username='parent1'
        )

        parent.email = 'parent1@school.com'
        parent.role = 'parent'
        parent.set_password('parent123')
        parent.save()

        # -----------------------------
        # STUDENTS
        # -----------------------------

        students = []

        for i in range(1, 11):

            student, created = User.objects.get_or_create(
                username=f'student{i}'
            )

            student.email = f'student{i}@school.com'
            student.role = 'student'

            student.first_name = f'Student{i}'
            student.last_name = 'Rahman'

            student.set_password('student123')

            student.save()

            StudentProfile.objects.get_or_create(

                user=student,

                defaults={

                    'roll_number': i,

                    'class_level': 9,

                    'section': 'A',

                    'group': 'Science',

                    'father_name': 'Father',

                    'mother_name': 'Mother',

                    'address': 'Dhaka'
                }
            )

            students.append(student)

        # -----------------------------
        # PARENT LINK
        # -----------------------------

        ParentStudentLink.objects.get_or_create(
            parent=parent,
            student=students[0],
            relationship='Father'
        )

        ParentStudentLink.objects.get_or_create(
            parent=parent,
            student=students[1],
            relationship='Father'
        )

        # -----------------------------
        # SUBJECTS
        # -----------------------------

        subject_data = [

            ('Bangla', 'BAN101', 'compulsory'),

            ('English', 'ENG101', 'compulsory'),

            ('Mathematics', 'MAT101', 'compulsory'),

            ('Physics', 'PHY101', 'compulsory'),

            ('Chemistry', 'CHE101', 'compulsory'),

            ('ICT', 'ICT101', 'compulsory'),

            ('Higher Math', 'HM101', 'optional_4th'),
        ]

        subjects = []

        for name, code, subject_type in subject_data:

            subject, created = Subject.objects.get_or_create(

                code=code,

                defaults={

                    'name': name,

                    'subject_type': subject_type,

                    'group': 'Science',

                    'class_levels': [9, 10],

                    'has_practical': False,

                    'full_marks': 100
                }
            )

            subjects.append(subject)

        # -----------------------------
        # SUBJECT ASSIGNMENTS
        # -----------------------------

        for i, subject in enumerate(subjects):

            SubjectAssignment.objects.get_or_create(

                teacher=teachers[i % 3],

                subject=subject,

                class_level=9,

                section='A',

                academic_year=2025
            )

        # -----------------------------
        # EXAM
        # -----------------------------

        exam, created = Exam.objects.get_or_create(

            name='Half-Yearly 2025',

            defaults={

                'exam_type': 'half_yearly',

                'class_level': 9,

                'date': date.today()
            }
        )

        # -----------------------------
        # MARKS
        # -----------------------------

        for student in students:

            for subject in subjects:

                written = random.randint(40, 70)

                mcq = random.randint(10, 25)

                # TOPPER
                if student.username == 'student1':

                    written = 70
                    mcq = 25

                # FAIL STUDENT
                if (
                    student.username == 'student5'
                    and subject.code == 'MAT101'
                ):

                    written = 10
                    mcq = 5

                StudentMark.objects.update_or_create(

                    student=student,
                    exam=exam,
                    subject=subject,

                    defaults={

                        'marks_written': written,

                        'marks_mcq': mcq,
                    }
                )

            # CALCULATE RESULT
            calculate_student_result(
                student,
                exam
            )

        # -----------------------------
        # MERIT LIST
        # -----------------------------

        generate_merit_list(
            exam,
            class_level=9,
            section='A'
        )

        # -----------------------------
        # PUBLISH RESULT
        # -----------------------------

        exam.is_published = True
        exam.save()

        # -----------------------------
        # ATTENDANCE
        # -----------------------------

        today = date.today()

        for i in range(7):

            attendance_date = today - timedelta(days=i)

            for student in students:

                Attendance.objects.get_or_create(

                    student=student,

                    date=attendance_date,

                    defaults={

                        'status': random.choice([
                            'Present',
                            'Absent',
                            'Late'
                        ]),

                        'class_level': 9,

                        'section': 'A',

                        'marked_by': teachers[0]
                    }
                )

        # -----------------------------
        # OUTPUT
        # -----------------------------

        self.stdout.write(
            self.style.SUCCESS(
                '\nSeed completed successfully!\n'
            )
        )

        self.stdout.write('--------------------------------')

        self.stdout.write(
            'Admin: admin@school.com / admin123'
        )

        self.stdout.write(
            'Teacher: teacher1@school.com / teacher123'
        )

        self.stdout.write(
            'Student: student1@school.com / student123'
        )

        self.stdout.write(
            'Parent: parent1@school.com / parent123'
        )

        self.stdout.write('--------------------------------')