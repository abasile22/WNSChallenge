import re


class DataParser:

    @staticmethod
    def normalize_ingredients(ingredient):
        result = []
        for text in ingredient:
            text = text.lower().replace(",", ".").strip()
            match = re.search(r"(\d+(\.\d+)?)\s*(kg|g)", text)
            if match:
                qty = float(match.group(1))
                unit = match.group(3)
                grams = int(qty * 1000) if unit == "kg" else int(qty)
            else:
                grams = None
            if ":" in text:
                name = text.split(":")[0].strip()
            elif " de " in text:
                name = text.split(" de ", 1)[1].strip()
            else:
                name = re.sub(r"(\d+(\.\d+)?)\s*(kg|g)", "", text).strip()
            result.append({
                "name": name,
                "weight": grams
            })
        return result