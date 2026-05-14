from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from .serializers import RegisterSerializer, UserSerializer,CustomLoginSerializer


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    'message': 'User Registered Successfully'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
    



class LoginView(TokenObtainPairView):

    serializer_class = CustomLoginSerializer



class StudentProfileView(APIView):

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

        try:
            profile = user.studentprofile
        except Exception:
            return Response(
                {'error': 'Student profile not found'},
                status=404
            )

        data = {

            'id': user.id,

            'username': user.username,

            'email': user.email,

            'first_name': user.first_name,

            'last_name': user.last_name,

            'phone': user.phone,

            'roll_number': profile.roll_number,

            'class_level': profile.class_level,

            'section': profile.section,

            'group': profile.group,

            'father_name': profile.father_name,

            'mother_name': profile.mother_name,

            'address': profile.address,
        }

        return Response(data)