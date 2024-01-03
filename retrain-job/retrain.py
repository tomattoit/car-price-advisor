import os
import psycopg2
import pandas as pd
import pickle

from catboost import CatBoostRegressor
from psycopg2 import sql

db_config = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_SERVICE": os.environ["POSTGRES_SERVICE"],
    "POSTGRES_DB": os.environ["POSTGRES_DB"],
}

columns = [
    "brand",
    "price",
    "year",
    "mileage",
    "capacity",
    "horse_power",
    "fuel_type",
    "transmission",
    "number_of_doors",
    "color",
    "origin_country",
    "no_accidents",
    "aso",
    "is_used",
]

DIRECTORY = "/app"
MODEL_FILE_NAME = "catboost.pkl"


class RetrainModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_config["POSTGRES_SERVICE"],
            database=db_config["POSTGRES_DB"],
            user=db_config["POSTGRES_USER"],
            password=db_config["POSTGRES_PASSWORD"],
            port=5432,
        )
        self.cursor = self.conn.cursor()

    def get_data(self):
        query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            sql.Identifier("cars"),
        )
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def _feature_engineering(self, df):
        df_copy = df.copy()
        df_copy["aso"].fillna(False, inplace=True)
        df_copy["brand"].fillna("Unknown", inplace=True)
        df_copy["origin_country"].fillna("Unknown", inplace=True)
        df_copy["no_accidents"].fillna(True, inplace=True)
        return df_copy

    def train_model(self, df):
        df = self._feature_engineering(df)
        X = df.drop(columns=["price"])
        y = df["price"]
        model = CatBoostRegressor(
            cat_features=[
                "brand",
                "origin_country",
                "color",
                "fuel_type",
                "transmission",
            ]
        )
        model.fit(X, y)
        return model

    def save_model(self, model):
        with open(os.path.join(DIRECTORY, "tmp.pkl"), "wb") as f:
            pickle.dump(model, f)
        os.replace(
            os.path.join(DIRECTORY, "tmp.pkl"),
            os.path.join(DIRECTORY, MODEL_FILE_NAME),
        )

    def retrain_model(self):
        data = self.get_data()
        df = pd.DataFrame(data, columns=columns)
        model = self.train_model(df)
        self.save_model(model)


if __name__ == "__main__":
    retrain = RetrainModel()
    retrain.retrain_model()
