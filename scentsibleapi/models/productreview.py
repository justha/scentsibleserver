from django.db import models

class ProductReview(models.Model):
    review_date = models.DateField()
    review = models.TextField()
    scentsibleuser = models.ForeignKey("ScentsibleUser", on_delete=models.CASCADE, related_name="productreviews")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="productreviews")
    rating = models.ForeignKey("Rating", on_delete=models.CASCADE, related_name="productreviews")



    @property
    def currentuser(self):
        return self.__currentuser

    @currentuser.setter
    def currentuser(self, value):
        self.__currentuser = value