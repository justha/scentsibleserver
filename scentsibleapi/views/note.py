"""View module for handling requests about Notes"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from scentsibleapi.models import Note

class Notes(ViewSet): 
    """ Responsible for GET """

    def list(self, request):
        """Handle GET requests to get all Notes
        Returns:Response -- JSON serialized list of Notes
        """
        notes = Note.objects.all()
        serializer = NoteSerializer(
            notes, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Note
        Returns: Response -- JSON serialized Note instance
        """
        try:           
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for related Django user"""
    class Meta: 
        model = Note
        fields = ['id', 'name']