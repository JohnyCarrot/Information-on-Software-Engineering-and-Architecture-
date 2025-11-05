from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, File, Form
from ninja.files import UploadedFile

from .models import Meal
from .schemas import MealIn, MealOut, MealUpdate

api = NinjaAPI(title="Wage-Donald API", csrf=False)


@api.get("/meals", response=List[MealOut])
def list_meals(request):
    return list(Meal.objects.all())


@api.get("/meals/{meal_id}", response=MealOut)
def get_meal(request, meal_id: int):
    return get_object_or_404(Meal, id=meal_id)


@api.post("/meals", response=MealOut)
def create_meal(
    request,
    payload: Form[MealIn],
    image: Optional[UploadedFile] = File(None),
):
    meal = Meal.objects.create(**payload.dict())
    if image:
        meal.image = image
        meal.save()
    return meal


@api.put("/meals/{meal_id}", response=MealOut)
def update_meal(
    request,
    meal_id: int,
    payload: Form[MealUpdate],
    image: Optional[UploadedFile] = File(None),
):
    meal = get_object_or_404(Meal, id=meal_id)

    for field, value in payload.dict().items():
        setattr(meal, field, value)

    if image is not None:
        meal.image = image

    meal.save()
    return meal


@api.delete("/meals/{meal_id}")
def delete_meal(request, meal_id: int):
    meal = get_object_or_404(Meal, id=meal_id)
    meal.delete()
    return {"success": True}
