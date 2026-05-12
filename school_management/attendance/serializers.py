from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Attendance

        fields = '__all__'




class AttendanceRecordSerializer(serializers.Serializer):

    student_id = serializers.IntegerField()

    status = serializers.ChoiceField(
        choices=[
            'Present',
            'Absent',
            'Late'
        ]
    )