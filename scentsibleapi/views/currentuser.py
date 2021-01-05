""" CurrentUser ViewSet Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from scentsibleapi.models import ScentsibleUser
from scentsibleapi.views.scentsibleuser import ScentsibleUserSerializer

class CurrentUser(ViewSet):
    """Responsible for GET"""

    def list(self, request):
        """ Handles GET to get current logged-in user 
        Returns: Response -- JSON serialized ScentsibleUser instance
        """

        #The code in the parentheses is like a WHERE clause in SQL
        user = ScentsibleUser.objects.get(user=request.auth.user)

        #Imported the RareUserSerializer from scentsibleuser.py to use in this module
        serializer = ScentsibleUserSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)