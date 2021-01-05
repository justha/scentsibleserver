"""Views module for handling requests about Products"""
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from scentsibleapi.models import Brand, Family, Group, Product, ScentsibleUser


class Products(ViewSet):
    """Responsible for GET, POST, PUT, DELETE"""
    
    def list(self, request):
        """Handle GET requests to get all ProductReviews"""
        products = Product.objects.all()
        creator_id = self.request.query_params.get('creator_id', None)
        group_id = self.request.query_params.get('group_id', None)
        brand_id = self.request.query_params.get('brand_id', None)
        family_id = self.request.query_params.get('family_id', None)

        for product in products:
            product.currentuser = None

            if product.creator.id == request.auth.user.id:
                product.currentuser = True
            else:
                product.currentuser = False
        
        if creator_id is not None:
            products = products.filter(creator_id=creator_id)

        if group_id is not None:
            products = products.filter(group_id=group_id)

        if brand_id is not None:
            products = products.filter(brand_id=brand_id)

        if family_id is not None:
            products = products.filter(family_id=family_id)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Product
        Returns: Response -- JSON serialized Product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            if product.creator.id == request.auth.user.id:
                product.currentuser = True
            else:
                product.currentuser = False
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations for Products
        Returns: Response -- JSON serialized Product instance
        """
        user = request.auth.user
        product = Product()

        try:
            product.name = request.data["name"]
            product.image_url = request.data["image_url"]
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(pk=request.data["group_id"])
            product.group_id = group.id
        except Group.DoesNotExist as ex:
            return Response({'message': 'Product type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            brand = Brand.objects.get(pk=request.data["brand_id"])
            product.brand_id = brand.id
        except Brand.DoesNotExist as ex:
            return Response({'message': 'Product type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            family = Family.objects.get(pk=request.data["family_id"])
            product.family_id = family.id
        except Family.DoesNotExist as ex:
            return Response({'message': 'Product type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        product.creator_id = user.id
        if creator is not None:
            try:
                product.save()
                serializer = ProductSerializer(product, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for Products
            Returns: Response -- Empty body with 204 status code
        """      
        scentsibleuser = ScentsibleUser.objects.get(user=request.auth.user)
        product = Product.objects.get(pk=pk)

        product.name = request.data["name"]
        product.image_url = request.data["image_url"]
        product.creator_id = scentsibleuser

        group = Product.objects.get(pk=request.data["group_id"])
        brand = Brand.objects.get(pk=request.data["brand_id"])
        family = Family.objects.get(pk=request.data["family_id"])
        product.group = request.data["group"]      
        product.brand = request.data["brand"]
        product.family = request.data["family"]
        

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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)

class ProductScentsibleUserSerializer(serializers.ModelSerializer):
    """Serializer for ScentsibleUser Info from a Product"""
    user = UserSerializer(many=False)

    class Meta:
        model = ScentsibleUser
        fields = ('id', 'user')

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for a Product"""
    creator = ProductScentsibleUserSerializer(many=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'image_url',
                  'creator_id', 'creator', 'group_id', 'group', 'brand_id', 'brand', 'family_id', 'family',
                  'currentuser')
        depth = 1
