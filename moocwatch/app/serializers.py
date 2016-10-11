from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from app.models import *
from app.api import *

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'url', 'course', 'description', 'image', 'provider')

class CourseTakerSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CourseTaker
        read_only_fields = ('user',)
        fields = ('id', 'user', 'course', 'status')
    
    def getuser(self):
        return self.context['request'].user
    
    def create(self, validated_data):
        courseTaker = CourseTaker(
            user = self.getuser(),
            course = validated_data['course'],
            status = validated_data['status']
        )
        courseTaker.full_clean(exclude=None)
        courseTaker.save()
        return courseTaker