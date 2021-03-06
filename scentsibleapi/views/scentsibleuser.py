"""Views module for handling requests about ScentsibleUsers"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from scentsibleapi.models import ScentsibleUser

class ScentsibleUsers(ViewSet):
    """ScentsibleUser Class"""

    def list(self, request):
        """Handles GET all"""
        users = ScentsibleUser.objects.all()

        serializer = ScentsibleUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single ScentsibleUser
        Returns:
            Response -- JSON serialized ScentsibleUser instance
        """
       
        try:
            user = ScentsibleUser.objects.get(pk=pk)
            
            #logic to set an unmapped property on ScentsibleUser 
            #will let front end determine if the user retrieved by this function is the current user
            if request.auth.user.id == int(pk):
                user.currentuser = True
            else:
                user.currentuser = False

            serializer = ScentsibleUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'date_joined', 'is_staff', 'is_active')

class ScentsibleUserSerializer(serializers.ModelSerializer):
    """Serializer for ScentsibleUser Info from a post"""
    user = UserSerializer(many=False)

    class Meta:
        model = ScentsibleUser
        fields = ('id', 'user', 'currentuser')