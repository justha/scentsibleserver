"""View module for handling requests about Families"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from scentsibleapi.models import Group

class Groups(ViewSet): 
    """ Responsible for GET """

    def list(self, request):
        """Handle GET requests to get all Groups
        Returns: Response -- JSON serialized list of Groups
        """
        groups = Group.objects.all()
        serializer = GroupSerializer(
            groups, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Group
        Returns: Response -- JSON serialized Group instance
        """
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class GroupSerializer(serializers.ModelSerializer):
    """JSON serializer for related Django user"""
    class Meta: 
        model = Group
        fields = ['id', 'name']