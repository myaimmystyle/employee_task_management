from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Tasks,Comments,Notifications


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("first_name","last_name")

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments 
        fields = ("task","comment")

class TaskSerializer(serializers.ModelSerializer):

    created_by = UserProfileSerializer(read_only=True)
    Tasks_Comments = CommentSerializer(many=True,read_only=True)

    class Meta:
        model = Tasks
        fields = ["id","task_name","task_status","created_on","created_by","Tasks_Comments"]

    def create(self, validated_data):
        validated_data['created_by'] = self.context.get("user_id")
        return Tasks.objects.create(**validated_data)

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications 
        fields = ("content","status")


