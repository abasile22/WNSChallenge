import sqlite3
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('db', check_same_thread=False)

    def insert_meal(self, meal):
        cursor = self.conn.execute("INSERT INTO meals (meal) VALUES (?)", (meal,))
        self.conn.commit()
        return cursor.lastrowid

    def insert_ingredients(self, ingredient, meal_id):
        self.conn.execute("INSERT INTO ingredients (ingredient, weight, meal_id) VALUES (?, ?, ?)",
                          (ingredient['name'], ingredient['weight'], meal_id))
        self.conn.commit()

    def insert_prices(self, name, price):
        self.conn.execute("INSERT INTO prices (ingredient, price) VALUES (?, ?)",
                          (name, price))
        self.conn.commit()

    def insert_recipe(self, recipe, meal_id):
        self.conn.execute("INSERT INTO recipes (recipe, meal_id) VALUES (?, ?)",
                          (recipe, meal_id))

        self.conn.commit()

    def get_meals(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        meals = self.conn.execute("SELECT meal FROM meals").fetchall()
        return meals

    def get_ingredients(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        meals = self.conn.execute("SELECT meal FROM meals").fetchall()
        return meals

    def get_prices(self):
        self.conn.row_factory = lambda cursor, row: row[0]
        prices = self.conn.execute("SELECT ingredient FROM prices").fetchall()
        return prices

    def delete_meals(self):
        self.conn.execute("DELETE FROM meals")
        self.conn.execute("DELETE FROM ingredients")
        self.conn.execute("DELETE FROM recipes")
        self.conn.execute("DELETE FROM prices")
        self.conn.commit()

    def get_ingredients_by_meal_name(self, meal_name):
        self.conn.row_factory = sqlite3.Row
        ingredients = self.conn.execute("SELECT i.ingredient, i.weight FROM meals m "
                                        "JOIN ingredients i ON m.id = i.meal_id "
                                        "WHERE meal = ?", (meal_name,)).fetchall()
        return [dict(row) for row in ingredients]

    def get_recipe_by_meal_name(self, meal_name):
        self.conn.row_factory = lambda cursor, row: row[0]
        recipe = self.conn.execute("SELECT r.recipe FROM meals m "
                                        "JOIN recipes r ON m.id = r.meal_id "
                                        "WHERE meal = ?", (meal_name,)).fetchall()
        return recipe

    def get_price_by_meal_name(self, meal_name):
        logger.info(f"Buscando precio para: '{meal_name}'")
        self.conn.row_factory = lambda cursor, row: row[0]
        result = self.conn.execute("SELECT price FROM prices m "
                                   "WHERE ingredient = ?", (meal_name,)).fetchone()
        logger.info(f"Resultado de búsqueda: {result}")

        # Ver todos los ingredientes en la tabla
        self.conn.row_factory = None
        all_prices = self.conn.execute("SELECT ingredient FROM prices").fetchall()
        logger.info(f"Ingredientes en precios: {all_prices}")

        return result

    def close(self):
        self.conn.commit()