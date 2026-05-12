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

        return Response(serializer.errors)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
    



class LoginView(TokenObtainPairView):

    serializer_class = CustomLoginSerializer