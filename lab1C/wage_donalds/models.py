from django.db import models

class Meal(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    calories = models.IntegerField()
    is_vegan = models.BooleanField(default=False)
    available_from = models.DateField()

    image = models.ImageField(upload_to="meals/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} ({self.price} €)"
