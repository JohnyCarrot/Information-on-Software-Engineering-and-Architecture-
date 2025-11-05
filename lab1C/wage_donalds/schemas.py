from ninja import ModelSchema, Schema
from typing import Optional
from .models import Meal
import datetime


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

class MealUpdate(Schema):
    name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    is_vegan: Optional[bool] = None
    available_from: Optional[datetime.date] = None
