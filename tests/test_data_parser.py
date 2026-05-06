import pytest
from app.shared.data_parser import DataParser


class TestDataParser:
    def setup_method(self):
        self.parser = DataParser()

    def test_normalize_ingredients_with_grams(self):
        ingredients = ["200g de tomate"]
        result = self.parser.normalize_ingredients(ingredients)

        assert len(result) == 1
        assert result[0]["name"] == "tomate"
        assert result[0]["weight"] == 200

    def test_normalize_ingredients_with_kilograms(self):
        ingredients = ["1.5kg de pollo"]
        result = self.parser.normalize_ingredients(ingredients)

        assert len(result) == 1
        assert result[0]["name"] == "pollo"
        assert result[0]["weight"] == 1500

    def test_normalize_ingredients_with_colon(self):
        ingredients = ["tomate: 300g"]
        result = self.parser.normalize_ingredients(ingredients)

        assert len(result) == 1
        assert result[0]["name"] == "tomate"
        assert result[0]["weight"] == 300

    def test_normalize_ingredients_without_weight(self):
        ingredients = ["tomate"]
        result = self.parser.normalize_ingredients(ingredients)

        assert len(result) == 1
        assert result[0]["name"] == "tomate"
        assert result[0]["weight"] is None

    def test_normalize_ingredients_multiple(self):
        ingredients = ["200g de tomate", "500g de cebolla", "pollo"]
        result = self.parser.normalize_ingredients(ingredients)

        assert len(result) == 3
        assert result[0]["name"] == "tomate"
        assert result[1]["name"] == "cebolla"
        assert result[2]["name"] == "pollo"

    def test_normalize_ingredients_lowercase(self):
        ingredients = ["300G DE LECHUGA"]
        result = self.parser.normalize_ingredients(ingredients)

        assert result[0]["name"] == "lechuga"
        assert result[0]["weight"] == 300

    def test_normalize_ingredients_with_comma_to_point(self):
        ingredients = ["1,5kg de arroz"]
        result = self.parser.normalize_ingredients(ingredients)

        assert result[0]["name"] == "arroz"
        assert result[0]["weight"] == 1500

    def test_normalize_ingredients_empty_list(self):
        ingredients = []
        result = self.parser.normalize_ingredients(ingredients)

        assert result == []
