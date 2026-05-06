import pytest
from app.domain.entities import Ingredient, Meal, Price, MealData


class TestIngredient:
    def test_ingredient_creation(self):
        ingredient = Ingredient(ingredient="tomate", weight=200)

        assert ingredient.ingredient == "tomate"
        assert ingredient.weight == 200

    def test_ingredient_with_none_weight(self):
        ingredient = Ingredient(ingredient="sal", weight=None)

        assert ingredient.ingredient == "sal"
        assert ingredient.weight is None


class TestMeal:
    def test_meal_creation(self):
        ingredients = [
            Ingredient(ingredient="tomate", weight=200),
            Ingredient(ingredient="cebolla", weight=150)
        ]
        meal = Meal(meal="Ensalada", ingredients=ingredients, recipe="Mezclar todo")

        assert meal.meal == "Ensalada"
        assert len(meal.ingredients) == 2
        assert meal.recipe == "Mezclar todo"

    def test_meal_with_empty_ingredients(self):
        meal = Meal(meal="Sopa", ingredients=[], recipe="Hervir agua")

        assert meal.meal == "Sopa"
        assert meal.ingredients == []


class TestPrice:
    def test_price_creation(self):
        price = Price(name="tomate", price=2.50)

        assert price.name == "tomate"
        assert price.price == 2.50

    def test_price_with_zero(self):
        price = Price(name="sal", price=0.0)

        assert price.price == 0.0


class TestMealData:
    def test_meal_data_creation(self):
        ingredients = [Ingredient(ingredient="tomate", weight=200)]
        meal_data = MealData(
            ingredients=ingredients,
            recipe="Preparar",
            total_value=10.50,
            total_value_usd=12.00
        )

        assert meal_data.total_value == 10.50
        assert meal_data.total_value_usd == 12.00
        assert len(meal_data.ingredients) == 1

    def test_meal_data_with_empty_ingredients(self):
        meal_data = MealData(
            ingredients=[],
            recipe="",
            total_value=0.0,
            total_value_usd=0.0
        )

        assert meal_data.ingredients == []
        assert meal_data.total_value == 0.0
