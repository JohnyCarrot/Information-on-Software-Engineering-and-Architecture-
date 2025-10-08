from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from api.models import Cheese
from api.schemas import CheeseOut, CheeseIn, CheeseUpdate, MilkType

api = NinjaAPI()

def basic_output(obj: Cheese) -> CheeseOut:
    return CheeseOut(
        id=obj.id,
        name=obj.name,
        milk_type=MilkType(obj.milk_type),
        expiration_date=obj.expiration_date,
        price_eur_per_kg=float(obj.price_eur_per_kg),
        country_of_origin=str(obj.country_of_origin),
    )
@api.get("/health")
def health(request):
    return {"status": "Im alive"}

@api.get("/list", response=list[CheeseOut])
def list_cheeses(request):
    return [basic_output(c) for c in Cheese.objects.all()]

@api.get("/{cheese_id}", response=CheeseOut)
def get_cheese(request, cheese_id: int):
    obj = get_object_or_404(Cheese, id=cheese_id)
    return basic_output(obj)

@api.post("/create", response=CheeseOut)
def create_cheese(request, payload: CheeseIn):
    obj = Cheese.objects.create(**payload.dict())
    return basic_output(obj)

@api.put("/{cheese_id}", response=CheeseOut)
def update_cheese(request, cheese_id: int, payload: CheeseIn):
    obj = get_object_or_404(Cheese, id=cheese_id)
    for field, value in payload.dict().items():
        setattr(obj, field, value)
    obj.save()
    return basic_output(obj)

@api.patch("/{cheese_id}", response=CheeseOut)
def partial_update_cheese(request, cheese_id: int, payload: CheeseUpdate):
    obj = get_object_or_404(Cheese, id=cheese_id)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    obj.save()
    return basic_output(obj)

@api.delete("/{cheese_id}", response=dict)
def delete_cheese(request, cheese_id: int):
    obj = get_object_or_404(Cheese, id=cheese_id)
    obj.delete()
    return {"success": True}