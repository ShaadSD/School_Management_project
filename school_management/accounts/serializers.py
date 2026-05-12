from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .models import (
    User,
    StudentProfile,
    TeacherProfile
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)



class CustomLoginSerializer(
    TokenObtainPairSerializer
):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    username = None

    def validate(self, attrs):

        email = attrs.get('email')

        password = attrs.get('password')

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            raise AuthenticationFailed(
                'Invalid email or password'
            )

        authenticated_user = authenticate(
            username=user.username,
            password=password
        )

        if not authenticated_user:

            raise AuthenticationFailed(
                'Invalid email or password'
            )

        self.user = authenticated_user

        refresh = self.get_token(authenticated_user)

        access = refresh.access_token

        response_data = {

            'id': authenticated_user.id,

            'username': authenticated_user.username,

            'email': authenticated_user.email,

            'role': authenticated_user.role,
        }

        return {

            'refresh': str(refresh),

            'access': str(access),

            'user': response_data
        }

class RegisterSerializer(serializers.ModelSerializer):

    # STUDENT FIELDS
    roll_number = serializers.IntegerField(
        required=False
    )

    class_level = serializers.IntegerField(
        required=False
    )

    section = serializers.CharField(
        required=False
    )

    father_name = serializers.CharField(
        required=False
    )

    mother_name = serializers.CharField(
        required=False
    )

    address = serializers.CharField(
        required=False
    )

    # TEACHER FIELDS
    employee_id = serializers.CharField(
        required=False
    )

    department = serializers.CharField(
        required=False
    )

    designation = serializers.CharField(
        required=False
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password',
            'role',
            'first_name',
            'last_name',

            # student
            'roll_number',
            'class_level',
            'section',
            'father_name',
            'mother_name',
            'address',

            # teacher
            'employee_id',
            'department',
            'designation',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):



        roll_number = validated_data.pop(
            'roll_number',
            None
        )

        class_level = validated_data.pop(
            'class_level',
            None
        )

        section = validated_data.pop(
            'section',
            None
        )

        father_name = validated_data.pop(
            'father_name',
            None
        )

        mother_name = validated_data.pop(
            'mother_name',
            None
        )

        address = validated_data.pop(
            'address',
            None
        )

        employee_id = validated_data.pop(
            'employee_id',
            None
        )

        department = validated_data.pop(
            'department',
            None
        )

        designation = validated_data.pop(
            'designation',
            None
        )



        password = validated_data.pop(
            'password'
        )

        user = User(**validated_data)

        user.set_password(password)

        user.save()



        if user.role == 'student':

            StudentProfile.objects.create(

                user=user,

                roll_number=roll_number,

                class_level=class_level,

                section=section,

                father_name=father_name,

                mother_name=mother_name,

                address=address
            )

        elif user.role == 'teacher':

            TeacherProfile.objects.create(

                user=user,

                employee_id=employee_id,

                department=department,

                designation=designation
            )

        return user
    













class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'