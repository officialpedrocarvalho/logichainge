from app import validators
from app.models import Task
from app.serializers import TaskSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# View for getting a list of tasks (incomplete, needs pagination and filtering)
class TaskListView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# View for creating a task
class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # Incomplete: Add validation for title and description (title should be unique and not empty, description should not be empty and should be less than 1000 characters)
    def post(self, request):
        data = request.data

        title = data.get("title")
        description = data.get("description")

        validators.validate_title(title, request.user)
        validators.validate_description(description)

        task = Task.objects.create(
            title=title,
            description=description,
            user=request.user
        )

        return Response(TaskSerializer(task).data, status=201)


# Authentication: User login and JWT token generation
@api_view(['POST'])
def login(request):
    data = request.data
    user = User.objects.filter(username=data['username']).first()
    if user and user.check_password(data['password']):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    return Response({"error": "Invalid credentials"}, status=400)
