from rest_framework.decorators import action
from account.authentication import JWTAuthentication
from account.serializers import UserSerializer
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrIsSelf
from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
# Create your views here.

class TestAPIView(APIView):
    # permission_classes = [IsAdminOrIsSelf]
    def get(self, request):
        user = request.user
        print(user)
        token = PasswordResetTokenGenerator.make_token(user)

        return Response({"token": token})
class UserLoginAPIView(APIView):
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email)
        if not user:
            raise exceptions.APIException('User not found')
        if not user.check_password(password):
            exceptions.APIException('Password is not exact')
        token = JWTAuthentication.generate_jwt(user.id)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'message': 'success'
        }
        return response
class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password is not matched')
        data.pop('password_confirm')
        user = User.objects.create_user(**data)
        return Response(UserSerializer(user).data)

class UserViewSet(viewsets.ModelViewSet):    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]
    #disable create  
    def create(self, request):
        pass

    def update(self, request, pk):    
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def info(self, request):
        print(request.user.last_login)
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['POST'])
    def change_password(self, request):
        data = request.data
        if data['new_password'] != data['new_password_confirm']:
            raise exceptions.APIException('Password not match')
        if request.user.check_password(data['old_password']):
            request.user.set_password(data['new_password'])
        return Response({
            "message": "Password has changed"
        })
    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        pass


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        
        print(self.action)
        if self.action in ('update', 'delete'):
            permission_classes = [IsAdminOrIsSelf]
        elif self.action in ('info', 'change_password'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
    