from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User


class ClientListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']


class ClientCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    


# getting the clients

class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by']

class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)  # Nested serializer for projects

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']


# Update info of a client

class ClientUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']


# Creating new project and assign client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.ListField(write_only=True, child=serializers.IntegerField())

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'user_ids', 'created_at', 'created_by']
        read_only_fields = ['id', 'client', 'created_at', 'created_by']

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids', [])
        client = validated_data.pop('client')
        created_by = validated_data.pop('created_by')
        project = Project.objects.create(client=client, created_by=created_by, **validated_data)

        users = User.objects.filter(id__in=user_ids)
        project.users.set(users)

        return project


