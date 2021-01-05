"""View module for handling requests about Brands"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from scentsibleapi.models import Brand

class Brands(ViewSet): 
    """ Responsible for GET """

    def list(self, request):
        """Handle GET requests to get all Brands
        Returns: Response -- JSON serialized list of Brands
        """
        brands = Brand.objects.all()
        serializer = BrandSerializer(
            brands, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Brand
        Returns: Response -- JSON serialized Brand instance
        """
        try:
            brand = Brand.objects.get(pk=pk)
            serializer = BrandSerializer(brand, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class BrandSerializer(serializers.ModelSerializer):
    """JSON serializer for related Django user"""
    class Meta: 
        model = Brand
        fields = ['id', 'name']