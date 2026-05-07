import re
import logging

import pytesseract
from PIL import ImageEnhance
from pdf2image import convert_from_bytes

logger = logging.getLogger(__name__)

class OCR:
    def __init__(self, file_bytes):
        self.file_bytes = file_bytes

    def read(self):
        try:
            pages = convert_from_bytes(self.file_bytes, dpi=300)
            lines = self._extract_text_from_pages(pages)
            return self._parse_lines(lines)
        except Exception as e:
            return []

    def _extract_text_from_pages(self, pages):
        lines = []
        for page in pages:
            text = pytesseract.image_to_string(
                self._preprocess_image(page),
                lang="spa",
                config="--oem 3 --psm 11"
            )
            lines += [l.strip() for l in text.split("\n") if l.strip()]
        return lines

    def _preprocess_image(self, img):
        img = img.convert("L")
        img = ImageEnhance.Contrast(img).enhance(1.5)
        return img

    def _parse_lines(self, lines):
        results = []
        current_name = None
        for line in lines:
            price_match = re.search(r"\$\s*([\d\.\,]+)", line)
            if price_match and current_name:
                price = int(price_match.group(1).replace(".", "").replace(",", ""))
                results.append({
                    "name": current_name.lower(),
                    "price": price
                })
                current_name = None
                continue
            if self._is_name(line):
                current_name = line
        return results

    def _is_name(self, line):
        return bool(re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+$", line))