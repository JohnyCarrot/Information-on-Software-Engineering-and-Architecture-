from django.db import models

class Pokemon(models.Model):
    TYPES = [
        ('fire', 'Fire'),
        ('water', 'Water'),
        ('grass', 'Grass'),
        ('electric', 'Electric'),
        ('normal', 'Normal'),
        ('rock', 'Rock'),
    ]

    name = models.CharField("Name",blank=True, null=True)
    type = models.CharField("Type", choices=TYPES, blank=True, null=True)
    level = models.IntegerField("Level", blank=True, null=True)
    hp = models.IntegerField("HP", blank=True, null=True)
    note = models.TextField("Description", blank=True, null=True)
    image = models.ImageField("Image", upload_to="pokemons/", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
