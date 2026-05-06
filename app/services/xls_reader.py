import io

import pandas as pd

from app.services.services import Services


class ExcelReader(Services):

    def read(self):
        file = io.BytesIO(self.file_bytes)
        df1 = pd.read_excel(file, usecols = 'C:D', skiprows=3, nrows=10, names=["name", "price"], dtype=str)
        df2 = pd.read_excel(file, usecols='C:D', skiprows=15, nrows=5, header=None, names=["name", "price"], dtype=str)
        df3 = pd.read_excel(file, usecols='C:D', skiprows=21, nrows=6, header=None, names=["name", "price"], dtype=str)
        df4 = pd.read_excel(file, usecols='F:G', skiprows=3, nrows=8, header=None, names=["name", "price"], dtype=str)
        df = pd.concat([df1, df2, df3, df4])
        df = df.dropna(subset=['price'])
        df['price'] = (df["price"].astype(str).str.replace("$", ""))
        df['price'] = (df["price"].astype(str).str.replace(".", ""))
        df['price'] = (df["price"].astype(int))
        df['name'] = (df["name"].astype(str).str.lower())
        return df.to_dict(orient="records")