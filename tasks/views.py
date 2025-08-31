from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now

from django.contrib.auth.models import User
from .models import Task
from .serializers import UserSerializer, TaskSerializer


# -------------------------------
# User ViewSet (CRUD)
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # التسجيل مسموح بدون login


# -------------------------------
# Task ViewSet (CRUD + Complete/Incomplete)
# -------------------------------
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # يرجع بس التاسكات الخاصة باليوزر الحالي
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # يربط التاسك باليوزر اللي عامل login
        serializer.save(owner=self.request.user)

    # Endpoint إضافي: Mark Complete
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = "Completed"
        task.completed_at = now()
        task.save()
        return Response(TaskSerializer(task).data)

    # Endpoint إضافي: Mark Incomplete
    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        task.status = "Pending"
        task.completed_at = None
        task.save()
        return Response(TaskSerializer(task).data)

