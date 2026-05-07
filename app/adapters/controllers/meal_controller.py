import logging
from flask import jsonify
from app.use_cases.get_meal_data import GetMealDataUseCase
from app.adapters.repositories.meal_repository import MealRepository

logger = logging.getLogger(__name__)

class MealController:
    def __init__(self):
        self.meal_repository = MealRepository()
        self.get_meal_data_use_case = GetMealDataUseCase(self.meal_repository)

    def get_meal_data(self, meal_name: str, date: str):
        try:
            meal_data = self.get_meal_data_use_case.execute(meal_name, date)

            return jsonify({
                "ingredients": [
                    {
                        "ingredient": ing.ingredient,
                        "weight": ing.weight
                    }
                    for ing in meal_data.ingredients
                ],
                "recipe": meal_data.recipe,
                "total_value": f"${meal_data.total_value:.2f}",
                "total_value_usd": f"${meal_data.total_value_usd:.2f}"
            })
        except Exception as e:
            logger.error(f"Error en get_meal_data: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 400

    def get_all_meals(self):
        meals = self.meal_repository.get_all_meals()
        return meals
