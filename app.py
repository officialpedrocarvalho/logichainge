# app.py

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
import json


# Task Model
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Serializer for Task model (incomplete, needs to be implemented)
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# View for getting a list of tasks (incomplete, needs pagination and filtering)
class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)  # Incomplete: Add pagination and sorting
        return Response(TaskSerializer(tasks, many=True).data)


# View for creating a task
class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # Incomplete: Add validation for title and description (title should be unique and not empty, description should not be empty and should be less than 1000 characters)
    def post(self, request):
        data = request.data
        task = Task.objects.create(
            title=data["title"],
            description=data["description"],
            user=request.user
        )
        return Response(TaskSerializer(task).data, status=201)


# Authentication: User login and JWT token generation
@api_view(['POST'])
def login(request):
    data = request.data
    user = User.objects.filter(username=data['username']).first()
    if user and user.check_password(data['password']):
        # Token creation logic missing
        return Response()
    return Response({"error": "Invalid credentials"}, status=400)
