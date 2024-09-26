from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if user with the given email already exists
        if User.objects.filter(email=email).exists():
            
            content_data = {
                'provide_by': "SMS API services",
                'success': False,
                'status': 400,
                'message': 'User with this email already exists'
            }
            return Response(content_data)

        # Create the user using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return response with token
        content_data = {
            'provide_by': "SMS API services",
            'success': True,
            'status': 200,
            'token': token.key,
            'data': serializer.data
        }
        return Response(content_data)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
