from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
import pandas as pd
import pickle
import os

df = pd.read_csv("output.csv")
df["aso"].fillna(False, inplace=True)
df["brand"].fillna("Unknown", inplace=True)
df["origin_country"].fillna("Unknown", inplace=True)
df.drop("type", axis=1, inplace=True)
df["no_accidents"].fillna(True, inplace=True)

param_grid = {
    "iterations": [500, 1000, 1500],
    "depth": [4, 6, 8, 10],
    "learning_rate": [0.01, 0.05, 0.1],
    "l2_leaf_reg": [1, 3, 5, 7, 9],
    "random_strength": [0.1, 0.5, 1],
    "bagging_temperature": [0.5, 1.0, 1.5],
    "border_count": [32, 64, 128],
}

model = CatBoostRegressor(
    cat_features=[
        "brand",
        "origin_country",
        "color",
        "fuel_type",
        "transmission",
    ]
)

# random_search = RandomizedSearchCV(
#     model, param_grid, n_iter=20, cv=3, verbose=2, random_state=42
# )

X, y = df.drop("price", axis=1), df["price"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model.fit(X_train, y_train)
# random_search.fit(X_train, y_train)
# best_params = random_search.best_params_
# print(best_params)
# best_model = random_search.best_estimator_
y_pred = model.predict(X_test)
print(mean_absolute_error(y_test, y_pred))

# save as pickle
with open("tmp.pkl", "wb") as f:
    pickle.dump(model, f)
os.replace("tmp.pkl", "catboost.pkl")
