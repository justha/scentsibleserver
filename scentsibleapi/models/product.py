from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=250)
    image_url = models.CharField(max_length=500)
    creator = models.ForeignKey("ScentsibleUser", on_delete=models.CASCADE, related_name="products")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, related_name="products")
    family = models.ForeignKey("Family", on_delete=models.CASCADE, related_name="products")


    @property
    def currentuser_created(self):
        return self.__currentuser_created

    @currentuser_created.setter
    def currentuser_created(self, value):
        self.__currentuser_created = value
        
    @property
    def currentuser_rated(self):
        return self.__currentuser_rated

    @currentuser_rated.setter
    def currentuser_rated(self, value):
        self.__currentuser_rated = value
    
    @property
    def currentuser_rating(self):
        return self.__currentuser_rating

    @currentuser_rating.setter
    def currentuser_rating(self, value):
        self.__currentuser_rating = value
    
    @property
    def average_rating(self):
        return self.__average_rating

    @average_rating.setter
    def average_rating(self, value):
        self.__average_rating = value
    