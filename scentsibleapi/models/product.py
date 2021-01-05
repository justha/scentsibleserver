from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=250)
    image_url = models.CharField(max_length=500)
    creator = models.ForeignKey("ScentsibleUser", on_delete=models.CASCADE, related_name="products")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, related_name="products")
    family = models.ForeignKey("Family", on_delete=models.CASCADE, related_name="products")


    @property
    def currentuser(self):
        return self.__currentuser

    @currentuser.setter
    def currentuser(self, value):
        self.__currentuser = value