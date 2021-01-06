"""View module for handling requests about Families"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from scentsibleapi.models import Family

class Families(ViewSet): 
    """ Responsible for GET """

    def list(self, request):
        """Handle GET requests to get all Families
        Returns: Response -- JSON serialized list of Families
        """
        families = Family.objects.all()
        serializer = FamilySerializer(
            families, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Family
        Returns: Response -- JSON serialized Family instance
        """
        try:           
            family = Family.objects.get(pk=pk)
            serializer = FamilySerializer(family, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class FamilySerializer(serializers.ModelSerializer):
    """JSON serializer for related Django user"""
    class Meta: 
        model = Family
        fields = ['id', 'name']