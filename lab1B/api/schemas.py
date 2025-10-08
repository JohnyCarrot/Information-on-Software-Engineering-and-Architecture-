from datetime import date
from enum import Enum
from typing import Optional
from ninja import Schema

class MilkType(str, Enum):
    COW = "COW"
    SHEEP = "SHEEP"
    GOAT = "GOAT"
    BUFFALO = "BUFFALO"
    OTHER = "OTHER"

class CheeseBase(Schema):
    name: str
    milk_type: MilkType
    expiration_date: date
    price_eur_per_kg: float
    country_of_origin: str  # "SK"

class CheeseIn(CheeseBase):
    pass

class CheeseOut(CheeseBase):
    id: int

class CheeseUpdate(Schema):
    name: Optional[str] = None
    milk_type: Optional[MilkType] = None
    expiration_date: Optional[date] = None
    price_eur_per_kg: Optional[float] = None
    country_of_origin: Optional[str] = None
