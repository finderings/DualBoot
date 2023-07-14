from rest_framework import serializers
from .models import User, Tag, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'email', 'date_of_birth', 'phone'
            )
            

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TaskSerializer(serializers.ModelSerilizer):
    author = UserSerializer()
    performer = UserSerializer()
    tags = TagSerializer()
    
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'date_created',
            'date_changed', 'final_date', 'status',
            'priority', 'author', 'performer', 'tags'
        )
