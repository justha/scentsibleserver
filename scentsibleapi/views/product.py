"""Views module for handling requests about Products"""
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from scentsibleapi.models import Product
from scentsibleapi.models import ScentsibleUser
from scentsibleapi.models import Category


class Products(ViewSet):

    def list(self, request):
    """ Handle GET requests to get all ProductReviews"""
        products = Product.objects.all()

        if not request.auth.user.is_staff:
            products = products.filter(approved = True).filter(publication_date__lt=date.today())
            
        for product in products:
            product.created_by_current_user = None

            if product.user.id == request.auth.user.id:
                product.created_by_current_user = True
            else:
                product.created_by_current_user = False

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            products = products.filter(user_id=user_id)

        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            products = products.filter(category_id=category_id)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Product
        Returns: Response -- JSON serialized Product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            if product.user.id == request.auth.user.id:
                poproductst.created_by_current_user = True
            else:
                product.created_by_current_user = False
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle Handle POST operations for Products
        Returns: Response -- JSON serialized Product instance
        """
        user = request.auth.user
        product = Product()

        try:
            product.title = request.data["title"]
            product.content = request.data["content"]
            product.publication_date = request.data["publication_date"]
            product.image_url = request.data["image_url"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        product.user_id = user.id

        try:
            category = Category.objects.get(pk=request.data["category_id"])
            product.category_id = category.id
        except Category.DoesNotExist as ex:
            return Response({'message': 'Product type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            try:
                product.save()
                serializer = ProductSerializer(product, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for Products"""
       
        scentsibleuser = ScentsibleUser.objects.get(user=request.auth.user)

        product = Product.objects.get(pk=pk)
        product.title = request.data["title"]
        product.publication_date = request.data["publication_date"]
        product.content = request.data["content"]
        product.image_url = request.data["image_url"]
        product.user = scentsibleuser

        category = Category.objects.get(pk=request.data["category_id"])
        product.category = category
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Product
        Returns: Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PUT'], detail=True)
    def approve(self, request, pk=None):

        product = Product.objects.get(pk=pk)

        product.approved = True
        product.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)

class ProductScentsibleUserSerializer(serializers.ModelSerializer):
    """Serializer for ScentsibleUser Info from a Product"""
    user = UserSerializer(many=False)

    class Meta:
        model = ScentsibleUser
        fields = ('id', 'bio', 'user')

class ProductSerializer(serializers.ModelSerializer):
    """Basic Serializer for a Product"""
    user = ProductScentsibleUserSerializer(many=False)

    class Meta:
        model = Product
        fields = ('id', 'title', 'publication_date', 'content',
                  'user', 'category_id', 'category', 'approved', 
                  'image_url', 'created_by_current_user')
        depth = 1
