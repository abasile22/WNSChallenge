from dataclasses import dataclass
from typing import List


@dataclass
class Ingredient:
    ingredient: str
    weight: int


@dataclass
class Meal:
    meal: str
    ingredients: List[Ingredient]
    recipe: str


@dataclass
class Price:
    name: str
    price: float


@dataclass
class MealData:
    ingredients: List[Ingredient]
    recipe: str
    total_value: float
    total_value_usd: float
