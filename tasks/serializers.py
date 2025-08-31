from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # عشان نعمل hash للباسورد
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


# -------------------------------
# Task Serializer
# -------------------------------
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # يظهر بس اسم صاحب التاسك

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date',
            'priority', 'status', 'completed_at',
            'owner', 'created_at', 'updated_at'
        ]
