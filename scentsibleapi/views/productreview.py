"""Views module for handling requests about ProductReviewss"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from scentsibleapi.models import ProductReview, Product, Rating


class ProductReviews(ViewSet):
    """ Responsible for GET, POST, DELETE """
    def list(self, request):
        """ Handle GET requests to get all ProductReviews"""
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
        """ Handle GET requests for single ProductReview
        Returns: Response -- JSON serialized ProductReview instance
        """
        try:
            brand = Brand.objects.get(pk=pk)
            serializer = ProductReviewSerializer(productreview, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """ Handle POST operations for ProductReviews
        Returns: Response -- JSON serialized ProductReview instance
        """

        #these match the properties in ReviewForm.js
        product_id = request.data["product_id"]
        rating_id = request.data["rating_id"]

        #check if product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message: invalid product id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        #check if Rating exists
        try:
            rating = Rating.objects.get(id=tag_id)
        except Rating.DoesNotExist:
            return Response({'message: invalid rating id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        #check if ProductReview exists
        try: 
            productreview = ProductReview.objects.get(product=product, rating=rating)
            return Response({'message': 'ProductReview already exists for these two items'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ProductReview.DoesNotExist:
            #if it does not exist, make new obj
            productreview = ProductReview()
            productreview.product = product
            productreview.rating = rating
            try: 
                productreview.save()
                serializer = ProductReviewSerializer(productreview, many=False, )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ Handle PUT requests for ProductReviews
        Returns: Response -- Empty body with 204 status code
        """
       
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
        """ Handle DELETE requests for a single ProductReview
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

class ProductReviewSerializer(serializers.ModelSerializer):
    """ Serializes ProductReviews """
    class Meta:
        model = ProductReview
        fields = ('id', 'product_id', 'product', 'rating_id', 'rating', 'review', 'review_date')
        depth = 3
        #so we can access whole rating and product object

