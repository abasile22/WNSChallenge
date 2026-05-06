import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from app.adapters.controllers.meal_controller import MealController
from app.domain.entities import Ingredient, MealData


class TestMealController:
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    @pytest.fixture
    def mock_meal_repository(self):
        return Mock()

    @pytest.fixture
    def mock_use_case(self):
        return Mock()

    def test_get_all_meals(self, mock_meal_repository):
        with patch('app.adapters.controllers.meal_controller.MealRepository', return_value=mock_meal_repository):
            with patch('app.adapters.controllers.meal_controller.GetMealDataUseCase'):
                mock_meal_repository.get_all_meals.return_value = ["Ensalada", "Sopa"]

                controller = MealController()
                result = controller.get_all_meals()

                assert result == ["Ensalada", "Sopa"]
                mock_meal_repository.get_all_meals.assert_called_once()

    def test_get_meal_data_success(self, app, mock_meal_repository):
        with app.app_context():
            with patch('app.adapters.controllers.meal_controller.MealRepository', return_value=mock_meal_repository):
                with patch('app.adapters.controllers.meal_controller.GetMealDataUseCase') as mock_use_case_class:
                    mock_use_case_instance = Mock()
                    mock_use_case_class.return_value = mock_use_case_instance

                    ingredients = [Ingredient(ingredient="tomate", weight=200)]
                    meal_data = MealData(
                        ingredients=ingredients,
                        recipe="Mezclar",
                        total_value=10.50,
                        total_value_usd=12.00
                    )
                    mock_use_case_instance.execute.return_value = meal_data

                    controller = MealController()
                    response = controller.get_meal_data("Ensalada", "2024-01-01")

                    assert response.status_code == 200
                    data = response.get_json()
                    assert data["total_value"] == "$10.50"
                    assert data["total_value_usd"] == "$12.00"
                    assert len(data["ingredients"]) == 1

    def test_get_meal_data_error(self, app, mock_meal_repository):
        with app.app_context():
            with patch('app.adapters.controllers.meal_controller.MealRepository', return_value=mock_meal_repository):
                with patch('app.adapters.controllers.meal_controller.GetMealDataUseCase') as mock_use_case_class:
                    mock_use_case_instance = Mock()
                    mock_use_case_class.return_value = mock_use_case_instance
                    mock_use_case_instance.execute.side_effect = Exception("Meal not found")

                    controller = MealController()
                    result = controller.get_meal_data("NoExiste", "2024-01-01")

                    # jsonify with status code returns a tuple (response, status_code)
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert status_code == 400
                        data = response.get_json()
                    else:
                        response = result
                        assert response.status_code == 400
                        data = response.get_json()
                    assert "error" in data
