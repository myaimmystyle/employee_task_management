from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.models import Token
from .serializers import TaskSerializer,UserProfileSerializer,CommentSerializer,NotificationSerializer
from core.models import Tasks,Comments,Notifications


class Login(APIView):
    
    def post(self,request):
        
        username = request.data.get('username',None)
        password = request.data.get('password',None)

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"message":"Login successfull","data":{"token":token.key,"staff":user.is_staff}},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Login failed"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message":"Login failed"},status=status.HTTP_400_BAD_REQUEST)

class Task(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        queryset = Tasks.objects.all()
        serializer = TaskSerializer(queryset,many=True)
        return Response({"message":"Task created","data":serializer.data},status=status.HTTP_200_OK)


    def post(self,request):
        serializer = TaskSerializer(data=request.data,context={'user_id': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Task created","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        instance = Tasks.objects.get(id=request.data.get('id'))
        instance.task_status = request.data.get('task_status')
        instance.task_time = (timezone.now() - instance.created_on).total_seconds()
        instance.save()
        return Response({"message":"Task updated","data":request.data},status=status.HTTP_200_OK)

class Comment(APIView):

    permission_classes = [permissions.IsAdminUser]

    def post(self,request):
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Task created","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class Notification(generics.ListAPIView):
    queryset = Notifications.objects.exclude(status='R')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]

    