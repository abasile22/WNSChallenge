from app.adapters.repositories.meal_repository import MealRepository
from app.domain.entities import MealData, Ingredient
from app.shared.utils import Utils


class GetMealDataUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        self.utils = Utils()

    def execute(self, meal_name: str, date: str) -> MealData:
        ingredients = self.meal_repository.get_ingredients_by_meal(meal_name)
        total = 0
        ingredient_list = []
        for ingredient in ingredients:
            price = self.meal_repository.get_price_by_name(ingredient['ingredient'])
            price_by_weight = self.utils.calculate_price(ingredient['weight'], price)
            total += price_by_weight
            ingredient_list.append(Ingredient(
                ingredient=ingredient['ingredient'].capitalize(),
                weight=ingredient['weight']
            ))
        ratio = self.utils.get_ratio_by_date(date)
        recipe = self.meal_repository.get_recipe_by_meal(meal_name)
        return MealData(
            ingredients=ingredient_list,
            recipe=recipe,
            total_value=total,
            total_value_usd=total / ratio
        )
