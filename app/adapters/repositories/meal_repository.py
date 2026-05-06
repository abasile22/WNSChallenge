from app.services.database import Database


class MealRepository:
    def __init__(self):
        self.db = Database()

    def insert_meal(self, meal_name: str) -> int:
        return self.db.insert_meal(meal_name)

    def insert_recipe(self, recipe: str, meal_id: int) -> None:
        self.db.insert_recipe(recipe, meal_id)

    def insert_ingredients(self, ingredient: dict, meal_id: int) -> None:
        self.db.insert_ingredients(ingredient, meal_id)

    def insert_prices(self, name: str, price: float) -> None:
        self.db.insert_prices(name, price)

    def delete_all_meals(self) -> None:
        self.db.delete_meals()

    def get_ingredients_by_meal(self, meal_name: str) -> list:
        return self.db.get_ingredients_by_meal_name(meal_name)

    def get_recipe_by_meal(self, meal_name: str) -> str:
        return self.db.get_recipe_by_meal_name(meal_name)

    def get_price_by_name(self, name: str) -> float:
        return self.db.get_price_by_meal_name(name)

    def get_all_meals(self) -> list:
        return self.db.get_meals()

    def get_all_prices(self) -> list:
        return self.db.get_prices()

    def close(self) -> None:
        self.db.close()
