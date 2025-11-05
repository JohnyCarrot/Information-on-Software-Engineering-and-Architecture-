from ninja import ModelSchema
from .models import Meal


class MealOut(ModelSchema):
    class Config:
        model = Meal
        model_fields = [
            "id",
            "name",
            "price",
            "calories",
            "is_vegan",
            "available_from",
            "image",
            "created_at",
        ]


class MealIn(ModelSchema):
    class Config:
        model = Meal
        model_fields = ["name", "price", "calories", "is_vegan", "available_from"]
