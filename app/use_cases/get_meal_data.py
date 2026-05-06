import logging
from app.adapters.repositories.meal_repository import MealRepository
from app.domain.entities import MealData, Ingredient
from app.shared.utils import Utils

logger = logging.getLogger(__name__)

class GetMealDataUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        self.utils = Utils()

    def execute(self, meal_name: str, date: str) -> MealData:
        ingredients = self.meal_repository.get_ingredients_by_meal(meal_name)
        total = 0
        prices = self.meal_repository.get_all_prices()
        logger.info(f"Prices: {prices}")
        ingredient_list = []
        for ingredient in ingredients:
            price = self.meal_repository.get_price_by_name(ingredient['ingredient'])

            logger.info(f"Ingrediente: {ingredient['ingredient']}, Precio: {price}")
            if price is None:
                logger.error(f"FALTA PRECIO para: {ingredient['ingredient']}")
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
