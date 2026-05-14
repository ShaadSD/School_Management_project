from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .models import Attendance

from .serializers import (
    AttendanceSerializer,
    AttendanceRecordSerializer
)

from academics.models import SubjectAssignment

from accounts.models import (
    StudentProfile,
    ParentStudentLink
)

User = get_user_model()



class MarkAttendanceView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if user.role != 'teacher':

            return Response(
                {
                    'error': 'Only teachers allowed'
                },
                status=403
            )

        class_level = request.data.get(
            'class_level'
        )

        section = request.data.get(
            'section'
        )

        date = request.data.get('date')

        records = request.data.get('records')

        if not class_level or not section or not date or not records:
            return Response(
                {'error': 'class_level, section, date, and records are required'},
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
                    'error': 'Not assigned teacher'
                },
                status=403
            )

        saved = []

        errors = []

        for row in records:

            serializer = AttendanceRecordSerializer(
                data=row
            )

            if serializer.is_valid():

                data = serializer.validated_data

                try:

                    student = User.objects.get(
                        id=data['student_id']
                    )

                except User.DoesNotExist:

                    errors.append({
                        'student_id': data['student_id'],
                        'error': 'Student not found'
                    })

                    continue

                attendance, created = Attendance.objects.update_or_create(

                    student=student,
                    date=date,

                    defaults={
                        'status': data['status'],
                        'class_level': class_level,
                        'section': section,
                        'marked_by': user
                    }
                )

                saved.append(student.username)

            else:

                errors.append(serializer.errors)

        return Response({
            'saved_count': len(saved),
            'error_count': len(errors),
            'errors': errors
        })
    



class MyAttendanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role != 'student':

            return Response(
                {
                    'error': 'Only students allowed'
                },
                status=403
            )

        from_date = request.GET.get(
            'from_date'
        )

        to_date = request.GET.get(
            'to_date'
        )

        attendance = Attendance.objects.filter(
            student=user
        )

        if from_date and to_date:

            attendance = attendance.filter(
                date__range=[from_date, to_date]
            )

        total_days = attendance.count()

        present = attendance.filter(
            status='Present'
        ).count()

        absent = attendance.filter(
            status='Absent'
        ).count()

        late = attendance.filter(
            status='Late'
        ).count()

        percentage = 0

        if total_days > 0:

            percentage = (
                present / total_days
            ) * 100

        serializer = AttendanceSerializer(
            attendance,
            many=True
        )

        return Response({

            'records': serializer.data,

            'summary': {
                'total_days': total_days,
                'present': present,
                'absent': absent,
                'late': late,
                'percentage': round(
                    percentage,
                    2
                )
            }
        })
    



class SectionAttendanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        class_level,
        section
    ):

        user = request.user

        # ONLY TEACHER OR ADMIN
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

            # RETURN EMPTY ARRAY INSTEAD OF 403
            if not assigned:

                return Response([])

        date = request.GET.get('date')

        attendance = Attendance.objects.filter(
            class_level=class_level,
            section=section,
            date=date
        )

        serializer = AttendanceSerializer(
            attendance,
            many=True
        )

        return Response(serializer.data)





class ChildAttendanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):

        user = request.user

        if user.role != 'parent':

            return Response(
                {
                    'error': 'Only parents allowed'
                },
                status=403
            )

        linked = ParentStudentLink.objects.filter(
            parent=user,
            student_id=child_id
        ).exists()

        if not linked:

            return Response(
                {
                    'error': 'Child not linked'
                },
                status=403
            )

        attendance = Attendance.objects.filter(
            student_id=child_id
        )

        serializer = AttendanceSerializer(
            attendance,
            many=True
        )

        return Response(serializer.data)
    



class AttendanceReportView(APIView):

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

        month = request.GET.get('month')

        year = request.GET.get('year')

        class_level = request.GET.get(
            'class_level'
        )

        students = StudentProfile.objects.filter(
            class_level=class_level
        )

        data = []

        for profile in students:

            attendance = Attendance.objects.filter(
                student=profile.user,
                date__month=month,
                date__year=year
            )

            total = attendance.count()

            present = attendance.filter(
                status='Present'
            ).count()

            percentage = 0

            if total > 0:

                percentage = (
                    present / total
                ) * 100

            data.append({

                'student': profile.user.username,

                'roll': profile.roll_number,

                'section': profile.section,

                'attendance_percentage': round(
                    percentage,
                    2
                )
            })

        return Response(data)
    

