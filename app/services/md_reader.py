import io
import re

from app.services.services import Services


class MarkdownReader(Services):

    def read(self):
        f = io.StringIO(self.file_bytes.decode('utf-8')).readlines()
        meals = []
        current_meal = None
        ingredients = []
        recipe = ""
        mode = None
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                if current_meal:
                    meals.append({
                        "meal": current_meal,
                        "ingredients": ingredients,
                        "recipe": recipe.strip()
                    })
                current_meal = line[2:].strip()
                ingredients = []
                recipe = ""
                mode = None
            elif line.startswith("##"):
                mode = "recipe"
            elif re.match(r"^(-|\d+\.\s|[a-zA-Z]\.\s)", line):
                mode = "ingredients"
                clean = re.sub(r"^(-|\d+\.\s|[a-zA-Z]\.\s)", "", line).strip()
                ingredients.append(clean)
            elif mode == "recipe":
                recipe += line + " "
        if current_meal:
            meals.append({
                "meal": current_meal,
                "ingredients": ingredients,
                "recipe": recipe.strip()
            })

        return meals