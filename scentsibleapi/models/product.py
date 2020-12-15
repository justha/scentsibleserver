from django.db import models

class Product(models.Model):
    creator = models.ForeignKey("ScentsibleUser", on_delete=models.CASCADE, related_name="products")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=250)
    family = models.ForeignKey("Family", on_delete=models.CASCADE, related_name="products")