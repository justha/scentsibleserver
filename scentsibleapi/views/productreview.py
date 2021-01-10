"""Views module for handling requests about ProductReviewss"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from scentsibleapi.models import ProductReview, Product, Rating, ScentsibleUser


class ProductReviews(ViewSet):
    """ Responsible for GET, POST, PUT, DELETE"""
    
    def list(self, request):
        """Handle GET requests to get all ProductReviews"""
        productreviews = ProductReview.objects.all()

        product_id = self.request.query_params.get("product_id", None)
        rating_id = self.request.query_params.get("rating_id", None)

        if product_id is not None:
            productreviews = productreviews.filter(product_id=product_id)
        
        if rating_id is not None:
            productreviews = productreviews.filter(rating_id=rating_id)
        
        serializer = ProductReviewSerializer(productreviews, many=True, context={'request', request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single ProductReview
        Returns: Response -- JSON serialized ProductReview instance
        """
        try:
            brand = Brand.objects.get(pk=pk)
            serializer = ProductReviewSerializer(productreview, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations for ProductReviews
        Returns: Response -- JSON serialized ProductReview instance
        """
        user = request.auth.user
        productreview = ProductReview()
        
        #Check if the following exist: Product, Rating, dictionary keys
        
        #These will match the properties in ReviewForm.js
        product_id = request.data["product_id"]
        rating_id = request.data["rating_id"]
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message: invalid product id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            rating = Rating.objects.get(id=rating_id)
        except Rating.DoesNotExist:
            return Response({'message: invalid rating id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            productreview.review = request.data["review"]
            productreview.review_date = request.data["review_date"]
        except KeyError as ex:
            return Response({'message': 'incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        #Check if this ProductReiew already exists
        try: 
            productreview = ProductReview.objects.get(product=product, rating=rating)
            return Response({'message': 'user has already reviewed this product'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ProductReview.DoesNotExist:
            #If it does not exist, create a new object

            productreview.product = product
            productreview.rating = rating
            productreview.scentsibleuser_id = user.id

            if user is not None:
                try: 
                    productreview.save()
                    serializer = ProductReviewSerializer(productreview, many=False, )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except ValidationError as ex:
                    return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for ProductReviews
        Returns: Response -- Empty body with 204 status code
        """       
        scentsibleuser = ScentsibleUser.objects.get(user=request.auth.user)
        productreview = ProductReview.objects.get(pk=pk)

        productreview.review_date = request.data["review_date"]
        productreview.review = request.data["review"]
        productreview.scentsibleuser = scentsibleuser

        product = Product.objects.get(pk=request.data["product_id"])
        rating = Rating.objects.get(pk=request.data["rating_id"])

        productreview.product = product
        productreview.rating = rating


        if product.creator.id == user.id:
            try:
                productreview.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single ProductReview
        Returns: Response -- 204, 404, or 500 status code
        """
        try:
            productreview = ProductReview.objects.get(pk=pk)
            productreview.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except ProductReview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)

class ProductReviewScentsibleUserSerializer(serializers.ModelSerializer):
    """Serializer for ScentsibleUser Info from a Product"""
    user = UserSerializer(many=False)

    class Meta:
        model = ScentsibleUser
        fields = ('id', 'user')

class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for ProductReviews"""
    scentsibleuser = ProductReviewScentsibleUserSerializer(many=False)

    class Meta:
        model = ProductReview
        fields = ('id', 'review_date', 'review', 
                'rating_id', 'rating',
                'scentsibleuser_id', 'scentsibleuser', 
                'product_id', 'product')
        depth = 2
        #To access product, rating and user user objects

