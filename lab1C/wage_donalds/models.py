from django.db import models

class Meal(models.Model):
    name = models.CharField(max_length=120,blank=True,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True,default=0)
    calories = models.IntegerField(default=0,blank=True,null=True)
    is_vegan = models.BooleanField(default=False,blank=True,null=True)
    available_from = models.DateField(blank=True,null=True)

    image = models.ImageField(upload_to="meals/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} ({self.price} €)"
