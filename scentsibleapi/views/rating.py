"""View module for handling requests about Ratings"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from scentsibleapi.models import Rating

class Ratings(ViewSet): 
    """ Responsible for GET """

    def list(self, request):
        """Handle GET requests to get all Ratings
        Returns:Response -- JSON serialized list of Ratings
        """
        ratings = Rating.objects.all()
        serializer = RatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Rating
        Returns: Response -- JSON serialized Rating instance
        """
        try:           
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for related Django user"""
    class Meta: 
        model = Rating
        fields = ['id', 'name', 'weight']