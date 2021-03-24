from rest_framework import serializers

from .models import TodoList,ProjectCode

class ProjectCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCode
        fields = "__all__"

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     if validated_data.get('file'):
    #         instance.file = validated_data.get('file')
    #
    #     instance.save()
    #     return self.instance