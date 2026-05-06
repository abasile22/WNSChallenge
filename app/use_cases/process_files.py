import logging
from typing import List, Dict
from app.adapters.repositories.meal_repository import MealRepository
from app.services.md_reader import MarkdownReader
from app.shared.data_parser import DataParser
from app.services.xls_reader import ExcelReader
from app.services.ocr import OCR

logger = logging.getLogger(__name__)

class ProcessFilesUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    def execute(self, files: List[Dict]) -> None:
        if len(files) != 3:
            raise ValueError(f"Se requieren exactamente 3 archivos. Recibido: {len(files)}")

        self.meal_repository.delete_all_meals()

        for file in files:
            self._process_single_file(file)

    def _process_single_file(self, file: Dict) -> None:
        filename = file["filename"]
        content = file["content"]

        if "md" in filename:
            self._process_markdown(content)
            logger.info("Se proceso el md")
        elif "pdf" in filename:
            self._process_pdf(content)
            logger.info("Se proceso el pdf")
        elif "xls" in filename:
            self._process_excel(content)
            logger.info("Se proceso el xls")

    def _process_markdown(self, content: bytes) -> None:
        meals = MarkdownReader(content).read()
        logger.info(f"MEALS: {meals}")
        for meal in meals:
            meal_id = self.meal_repository.insert_meal(meal['meal'])
            ingredients = DataParser().normalize_ingredients(meal['ingredients'])
            self.meal_repository.insert_recipe(meal['recipe'], meal_id)
            for ingredient in ingredients:
                self.meal_repository.insert_ingredients(ingredient, meal_id)

    def _process_pdf(self, content: bytes) -> None:
        logger.info(f"LLEGA A FUNCION DE PROCESAMIENTO")
        prices = OCR(content).read()
        logger.info(f"PRICES: {prices}")
        for price in prices:
            logger.info(f"Price en OCR: {price}")
            self.meal_repository.insert_prices(price['name'], price['price'])

    def _process_excel(self, content: bytes) -> None:
        prices = ExcelReader(content).read()
        for price in prices:
            self.meal_repository.insert_prices(price['name'], price['price'])
