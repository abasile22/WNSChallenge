import io
import logging

import pandas as pd

logger = logging.getLogger(__name__)

class ExcelReader:
    def __init__(self, file_bytes):
        self.file_bytes = file_bytes

    def read(self):
        try:
            file = io.BytesIO(self.file_bytes)
            dfs = [
                pd.read_excel(file, usecols='C:D', skiprows=3, nrows=10, names=["name", "price"], dtype=str),
                pd.read_excel(file, usecols='C:D', skiprows=15, nrows=5, header=None, names=["name", "price"], dtype=str),
                pd.read_excel(file, usecols='C:D', skiprows=21, nrows=6, header=None, names=["name", "price"], dtype=str),
                pd.read_excel(file, usecols='F:G', skiprows=3, nrows=8, header=None, names=["name", "price"], dtype=str)
            ]
            df = pd.concat(dfs, ignore_index=True)
            df = df.dropna(subset=['price'])
            df = df[df['price'].astype(str).str.strip() != '']
            df = self._clean_prices(df)
            df = self._clean_names(df)
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            return []

    def _clean_prices(self, df):
        try:
            df['price'] = df['price'].astype(str).str.strip()
            df['price'] = df['price'].str.replace(r'[\$\s]', '', regex=True)
            df['price'] = df['price'].str.replace('.', '', n=1)
            df['price'] = df['price'].str.replace('.', '')
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df = df.dropna(subset=['price'])
            df['price'] = df['price'].astype(int)
        except Exception as e:
            logger.error(f"Error cleaning prices: {e}")
        return df

    def _clean_names(self, df):
        try:
            df['name'] = df['name'].astype(str).str.strip().str.lower()
            df = df[df['name'] != '']
        except Exception as e:
            logger.error(f"Error cleaning names: {e}")
        return df