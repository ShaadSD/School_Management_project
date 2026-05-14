from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from django.contrib.auth import get_user_model

from academics.models import (
    SubjectAssignment,
    Subject,
    Exam
)
from accounts.models import StudentProfile
from .models import StudentMark,StudentResult
from .serializers import (
    StudentMarkSerializer,
    BulkMarkSerializer,
    StudentResultSerializer
)
from .services import calculate_student_result,generate_merit_list

User = get_user_model()


class DashboardStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role != 'admin':

            return Response(
                {
                    'error': 'Only admin allowed'
                },
                status=403
            )

        total_students = User.objects.filter(
            role='student'
        ).count()

        total_teachers = User.objects.filter(
            role='teacher'
        ).count()

        total_parents = User.objects.filter(
            role='parent'
        ).count()

        total_subjects = Subject.objects.count()

        total_exams = Exam.objects.count()

        return Response({

            'total_students': total_students,

            'total_teachers': total_teachers,

            'total_parents': total_parents,

            'total_subjects': total_subjects,

            'total_exams': total_exams,
        })





class MarksEntryView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        # ONLY TEACHER
        if user.role != 'teacher':

            return Response(
                {
                    'error': 'Only teachers can enter marks'
                },
                status=403
            )

        serializer = StudentMarkSerializer(
            data=request.data
        )

        if serializer.is_valid():

            subject = serializer.validated_data['subject']

            student = serializer.validated_data['student']

            exam = serializer.validated_data['exam']

            # GET STUDENT PROFILE
            try:
                profile = student.studentprofile
            except Exception:
                return Response(
                    {'error': 'Student profile not found'},
                    status=400
                )

            # CHECK TEACHER ASSIGNMENT
            assigned = SubjectAssignment.objects.filter(
                teacher=user,
                subject=subject,
                class_level=profile.class_level,
                section=profile.section
            ).exists()

            if not assigned:

                return Response(
                    {
                        'error': 'You are not assigned'
                    },
                    status=403
                )

            mark = serializer.save()

            # AUTO GPA CALCULATION
            calculate_student_result(
                student,
                exam
            )

            return Response(
                StudentMarkSerializer(mark).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )
    




class BulkMarksEntryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role != 'teacher':

            return Response(
                {
                    'error': 'Only teachers allowed'
                },
                status=403
            )

        class_level = request.query_params.get(
            'class_level'
        )

        section = request.query_params.get(
            'section'
        )

        if not class_level or not section:

            return Response(
                {
                    'error': 'class_level and section are required'
                },
                status=400
            )

        # TEACHER ASSIGNMENT CHECK
        assigned = SubjectAssignment.objects.filter(
            teacher=user,
            class_level=class_level,
            section=section
        ).exists()

        if not assigned:

            return Response(
                {
                    'error': 'You are not assigned to this section'
                },
                status=403
            )

        students = StudentProfile.objects.filter(
            class_level=class_level,
            section=section
        ).select_related(
            'user'
        ).order_by(
            'roll_number'
        )

        data = []

        for profile in students:

            data.append({
                'student_id': profile.user.id,
                'full_name': profile.user.get_full_name(),
                'roll_number': profile.roll_number
            })

        return Response(data)



    def post(self, request):

        user = request.user

        if user.role != 'teacher':

            return Response(
                {
                    'error': 'Only teachers allowed'
                },
                status=403
            )

        subject_id = request.data.get('subject')

        exam_id = request.data.get('exam')

        records = request.data.get('records')

        if not records:

            return Response(
                {
                    'error': 'No records provided'
                },
                status=400
            )

        try:

            subject = Subject.objects.get(code=subject_id)

            exam = Exam.objects.get(id=exam_id)

        except (Subject.DoesNotExist, Exam.DoesNotExist):

            return Response(
                {
                    'error': 'Invalid subject or exam'
                },
                status=400
            )

        errors = []

        success = []

        for row in records:

            serializer = BulkMarkSerializer(data=row)

            if serializer.is_valid():

                data = serializer.validated_data

                try:

                    student = User.objects.get(
                        id=data['student_id'],
                        role='student'
                    )

                except User.DoesNotExist:

                    errors.append({
                        'student_id': data['student_id'],
                        'error': 'Student not found'
                    })

                    continue

                try:
                    profile = student.studentprofile
                except Exception:
                    errors.append({
                        'student_id': student.id,
                        'error': 'Student profile not found'
                    })
                    continue

                assigned = SubjectAssignment.objects.filter(
                    teacher=user,
                    subject=subject,
                    class_level=profile.class_level,
                    section=profile.section
                ).exists()

                if not assigned:

                    errors.append({
                        'student_id': student.id,
                        'error': 'Not assigned teacher'
                    })

                    continue

                written = data['marks_written']
                mcq = data['marks_mcq']
                practical = data.get(
                    'marks_practical',
                    0
                ) or 0

                if (
                    written < 0 or
                    mcq < 0 or
                    practical < 0
                ):

                    errors.append({
                        'student_id': student.id,
                        'error': 'Marks cannot be negative'
                    })

                    continue

                if (
                    subject.has_practical is False
                    and practical > 0
                ):

                    errors.append({
                        'student_id': student.id,
                        'error': 'This subject has no practical'
                    })

                    continue

                total = written + mcq + practical

                if total > subject.full_marks:

                    errors.append({
                        'student_id': student.id,
                        'error': 'Marks exceed full marks'
                    })

                    continue

                mark, created = StudentMark.objects.update_or_create(
                    student=student,
                    exam=exam,
                    subject=subject,

                    defaults={
                        'marks_written': written,
                        'marks_mcq': mcq,
                        'marks_practical': practical
                    }
                )

                calculate_student_result(
                    student,
                    exam
                )

                success.append({
                    'student_id': student.id,
                    'student': student.get_full_name()
                })

            else:

                errors.append(serializer.errors)

        return Response({
            'success_count': len(success),
            'error_count': len(errors),
            'success': success,
            'errors': errors
        })





class MyResultView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):

        user = request.user

        if user.role != 'student':

            return Response(
                {
                    'error': 'Only students allowed'
                },
                status=403
            )

        try:

            exam = Exam.objects.get(
                id=exam_id
            )

        except Exam.DoesNotExist:

            return Response(
                {
                    'error': 'Exam not found'
                },
                status=404
            )

        # RESULT MUST BE PUBLISHED
        if exam.is_published is False:

            return Response(
                {
                    'error': 'Result not published yet'
                },
                status=403
            )

        try:

            result = StudentResult.objects.get(
                student=user,
                exam=exam
            )

        except StudentResult.DoesNotExist:

            return Response(
                {
                    'error': 'Result not found'
                },
                status=404
            )

        serializer = StudentResultSerializer(result)

        return Response(serializer.data)
    




class SectionResultView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        exam_id,
        class_level,
        section
    ):

        user = request.user

        if user.role not in ['teacher', 'admin']:

            return Response(
                {
                    'error': 'Permission denied'
                },
                status=403
            )

        # TEACHER ASSIGNMENT CHECK
        if user.role == 'teacher':

            assigned = SubjectAssignment.objects.filter(
                teacher=user,
                class_level=class_level,
                section=section
            ).exists()

            if not assigned:

                return Response(
                    {
                        'error': 'Not assigned'
                    },
                    status=403
                )

        student_ids = StudentProfile.objects.filter(
            class_level=class_level,
            section=section
        ).values_list(
            'user_id',
            flat=True
        )

        results = StudentResult.objects.filter(
            exam_id=exam_id,
            student_id__in=student_ids
        ).order_by(
            'class_position'
        )

        serializer = StudentResultSerializer(
            results,
            many=True
        )

        return Response(serializer.data)
    



class MeritListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):

        user = request.user

        if user.role not in ['teacher', 'admin']:

            return Response(
                {
                    'error': 'Permission denied'
                },
                status=403
            )

        results = StudentResult.objects.filter(
            exam_id=exam_id
        ).order_by(
            'class_position'
        )

        serializer = StudentResultSerializer(
            results,
            many=True
        )

        return Response(serializer.data)
    



class PublishResultView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, exam_id):

        user = request.user

        if user.role != 'admin':

            return Response(
                {
                    'error': 'Only admin allowed'
                },
                status=403
            )

        try:

            exam = Exam.objects.get(id=exam_id)

        except Exam.DoesNotExist:

            return Response(
                {
                    'error': 'Exam not found'
                },
                status=404
            )

        # GET ALL STUDENTS WHO HAVE MARKS
        student_ids = StudentMark.objects.filter(
            exam=exam
        ).values_list(
            'student_id',
            flat=True
        ).distinct()

        # CALCULATE RESULT FOR EACH STUDENT
        for student_id in student_ids:

            student = User.objects.get(
                id=student_id
            )

            calculate_student_result(
                student,
                exam
            )

        # GENERATE MERIT LIST
        generate_merit_list(exam)

        # PUBLISH
        exam.is_published = True

        exam.save()

        return Response(
            {
                'message': 'Result published successfully'
            }
        )
    

