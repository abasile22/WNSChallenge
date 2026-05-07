import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def insert_meal(self, meal):
        try:
            cursor = self.conn.execute("INSERT INTO meals (meal) VALUES (?)", (meal,))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error inserting meal: {e}")
            self.conn.rollback()
            raise

    def insert_ingredients(self, ingredient, meal_id):
        try:
            self.conn.execute("INSERT INTO ingredients (ingredient, weight, meal_id) VALUES (?, ?, ?)",
                              (ingredient['name'], ingredient['weight'], meal_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error inserting ingredient: {e}")
            self.conn.rollback()
            raise

    def insert_prices(self, name, price):
        try:
            self.conn.execute("INSERT INTO prices (ingredient, price) VALUES (?, ?)",
                              (name, price))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error inserting price: {e}")
            self.conn.rollback()
            raise

    def insert_recipe(self, recipe, meal_id):
        try:
            self.conn.execute("INSERT INTO recipes (recipe, meal_id) VALUES (?, ?)",
                              (recipe, meal_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error inserting recipe: {e}")
            self.conn.rollback()
            raise

    def get_meals(self):
        try:
            cursor = self.conn.execute("SELECT meal FROM meals")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching meals: {e}")
            return []

    def delete_all_meals(self):
        try:
            self.conn.execute("DELETE FROM meals")
            self.conn.execute("DELETE FROM ingredients")
            self.conn.execute("DELETE FROM recipes")
            self.conn.execute("DELETE FROM prices")
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error deleting meals: {e}")
            self.conn.rollback()
            raise

    def get_ingredients_by_meal_name(self, meal_name):
        try:
            ingredients = self.conn.execute(
                "SELECT i.ingredient, i.weight FROM meals m "
                "JOIN ingredients i ON m.id = i.meal_id "
                "WHERE meal = ?", (meal_name,)).fetchall()
            return [dict(row) for row in ingredients]
        except Exception as e:
            logger.error(f"Error fetching ingredients: {e}")
            return []

    def get_recipe_by_meal_name(self, meal_name):
        try:
            recipe = self.conn.execute(
                "SELECT r.recipe FROM meals m "
                "JOIN recipes r ON m.id = r.meal_id "
                "WHERE meal = ?", (meal_name,)).fetchone()
            return recipe[0] if recipe else None
        except Exception as e:
            logger.error(f"Error fetching recipe: {e}")
            return None

    def get_price_by_ingredient(self, ingredient):
        try:
            result = self.conn.execute(
                "SELECT price FROM prices WHERE ingredient = ?",
                (ingredient,)).fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            return None

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")