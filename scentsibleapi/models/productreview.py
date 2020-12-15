from django.db import models

class ProductReview(models.Model):
    user = models.ForeignKey("ScentsibleUser", on_delete=models.CASCADE, related_name="productreviews")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="productreviews")
    rating = models.ForeignKey("Rating", on_delete=models.CASCADE, related_name="productreviews")
    review = models.TextField()
    review_date = models.DateField()
    quantity = models.IntegerField()