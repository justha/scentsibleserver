from django.db import models

class ProductReview(models.Model):
    review_date = models.DateField()
    review = models.TextField()
    scentsibleuser = models.ForeignKey("ScentsibleUser", on_delete=models.CASCADE, related_name="productreviews")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="productreviews")
    rating = models.ForeignKey("Rating", on_delete=models.CASCADE, related_name="productreviews")



    @property
    def currentuser_created(self):
        return self.__currentuser_created

    @currentuser_created.setter
    def currentuser_created(self, value):
        self.__currentuser_created = value