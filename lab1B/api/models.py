from django.db import models
from django_countries.fields import CountryField

class Cheese(models.Model):

    name = models.CharField(max_length=120)
    milk_type = models.CharField(max_length=10)
    expiration_date = models.DateField(help_text="Expiration date (best before)")
    price_eur_per_kg = models.DecimalField(max_digits=7, decimal_places=2)
    country_of_origin = CountryField(blank_label="(select country)")

    def __str__(self):
        return f"{self.name} ({self.milk_type})"
