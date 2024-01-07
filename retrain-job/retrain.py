import psycopg2
import pandas as pd
import pickle
import os
import time
import requests

from catboost import CatBoostRegressor
from psycopg2 import sql

db_config = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_SERVICE": os.environ["POSTGRES_SERVICE"],
    "POSTGRES_DB": os.environ["POSTGRES_DB"],
}

columns = [
    "aso",
    "brand",
    "capacity",
    "color",
    "fuel_type",
    "horse_power",
    "is_used",
    "mileage",
    "no_accidents",
    "number_of_doors",
    "origin_country",
    "transmission",
    "year",
    "price",
]

DIRECTORY = "/mnt/data"
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

    def save_model(self, model, version):
        with open(os.path.join(DIRECTORY, f"catboost_{version}.pkl"), "wb") as f:
            pickle.dump(model, f)

    def retrain_model(self, version):
        data = self.get_data()
        df = pd.DataFrame(data, columns=columns)
        model = self.train_model(df)
        self.save_model(model, version=version)


if __name__ == "__main__":
    retrain = RetrainModel()
    version = int(time.time())
    retrain.retrain_model(version=version)

    # send request to flask-api to update model
    flask_api_url = os.environ["FLASK_SERVICE"]
    r = requests.get(f"http://{flask_api_url}:5000/update/{version}")
