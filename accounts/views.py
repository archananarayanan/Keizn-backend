from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer, LoginSerializer, LoginDetailsSerializer
import datetime
from django.conf import settings
import jwt
from .models import User

@swagger_auto_schema(
        method='post',
        operation_description="Create new User",
        request_body=UserSerializer,
        security=[],
        tags=['Users'],
    )
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
        method='post',
        operation_description="Login User",
        request_body=LoginSerializer,
        security=[],
        tags=['Users'],
    )
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username, password=password).first()

        if user:
            user = LoginDetailsSerializer(user)
            auth_token = jwt.encode({'username': user.data.get('username'), 'userid': user.data.get('userid'),
                                     'exp': datetime.datetime.timestamp((datetime.datetime.now() + datetime.timedelta(days=1, hours=3)))},
                                    settings.SECRET_KEY, 'HS256')
            data = {
                'user': user.data, 'token': auth_token
            }
            return Response({'data':data, 'issuccess':True}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)



@swagger_auto_schema(
        method='post',
        operation_description="Logout User",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
            },
        ),
        security=[],
        tags=['Users'],
    )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@swagger_auto_schema(
        method='post',
        operation_description="Reset Password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Users'],
    )
@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        username = request.data.get('username')

        user = User.objects.get(username=username)
        if user:
            # user.set_password(request.data.get('password'))
            user.password = request.data.get('password')
            user.save(force_update=True)
            return Response("Success!", status=status.HTTP_201_CREATED)
        
        return Response("Unknown Error occured!", status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        user = User.objects.all()
        if user:
            serializer = UserSerializer(user, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response("Unknown Error occured!", status=status.HTTP_400_BAD_REQUEST)

