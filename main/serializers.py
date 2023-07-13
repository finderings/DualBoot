from rest_framework import serializers
from .models import User, Tag, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'email', 'date_of_birth', 'phone'
            )
        

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        Status = Task.Status
        model = Status
        fields = (
            'NEW_TASK', 'IN_DEVELOMENT', 'ARCHIVED',
            'IN_QA', 'IN_CODE_REvIEW',
            'READY_FOR_RELEASE', 'RELEASED'
        )
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TaskSerializer(serializers.ModelSerilizer):
    status = StatusSerializer()
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
