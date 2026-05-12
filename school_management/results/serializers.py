from rest_framework import serializers

from .models import StudentMark,StudentResult

from academics.models import SubjectAssignment


class StudentMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentMark

        fields = '__all__'

    def validate(self, data):

        subject = data['subject']

        written = data.get('marks_written', 0)
        mcq = data.get('marks_mcq', 0)
        practical = data.get('marks_practical', 0) or 0

        total = written + mcq + practical

        # FULL MARKS VALIDATION
        if total > subject.full_marks:

            raise serializers.ValidationError(
                'Total marks exceed full marks'
            )

        # PRACTICAL VALIDATION
        if (
            subject.has_practical is False
            and practical > 0
        ):

            raise serializers.ValidationError(
                'This subject has no practical marks'
            )

        return data
    




class BulkMarkSerializer(serializers.Serializer):

    student_id = serializers.IntegerField()

    marks_written = serializers.FloatField()

    marks_mcq = serializers.FloatField()

    marks_practical = serializers.FloatField(
        required=False,
        allow_null=True
    )




class StudentResultMarkSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(
        source='subject.name',
        read_only=True
    )

    subject_code = serializers.CharField(
        source='subject.code',
        read_only=True
    )

    class Meta:

        model = StudentMark

        fields = [
            'subject_name',
            'subject_code',
            'marks_written',
            'marks_mcq',
            'marks_practical',
            'total_marks',
            'letter_grade',
            'grade_point',
        ]



    
class StudentResultSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source='student.get_full_name',
        read_only=True
    )

    marks = serializers.SerializerMethodField()

    class Meta:

        model = StudentResult

        fields = [
            'student_name',
            'gpa',
            'total_marks',
            'class_position',
            'is_passed',
            'marks',
        ]

    def get_marks(self, obj):

        marks = StudentMark.objects.filter(
            student=obj.student,
            exam=obj.exam
        )

        return StudentResultMarkSerializer(
            marks,
            many=True
        ).data