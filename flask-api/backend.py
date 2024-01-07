from flask import Flask, request, jsonify
from flask_cors import CORS
from multiprocessing import Value
import gunicorn.app.base

import os
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app)

FEATURES = [
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
]
MODEL_DIRECTORY_PATH = "/mnt/data"

model = None
version = 0


def initialize():
    global shared_version
    shared_version = Value("i", 0)
    init_model()


def init_model():
    global model
    global shared_version
    global version
    model_pickle_path = os.path.join(
        MODEL_DIRECTORY_PATH, f"catboost_{shared_version.value}.pkl"
    )
    app.logger.error(f"Model path: {model_pickle_path}")
    if not os.path.exists(model_pickle_path):
        return
    version = shared_version.value
    with open(model_pickle_path, "rb") as f:
        model = pickle.load(f)
    app.logger.error(f"Model version: {version}")


@app.route("/api/predict", methods=["POST"])
def predict_endpoint():
    global version
    global shared_version
    if version != shared_version.value:
        init_model()
    if not model:
        return {"error": "Model not initialized"}, 500
    data = pd.json_normalize(request.json)[FEATURES]
    prediction = model.predict(data)[0]
    return jsonify(prediction)


@app.route("/update/<version_number>", methods=["GET"])
def update_model(version_number):
    global shared_version
    with shared_version.get_lock():
        shared_version.value = int(version_number)
    return {"status": "success"}, 200


@app.route("/api/version", methods=["GET"])
def get_version():
    global shared_version
    return {"version": shared_version.value, "pid": os.getpid()}, 200


class HttpServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self):
        super().run()


if __name__ == "__main__":
    global message_queue
    options = {
        "bind": "%s:%s" % ("0.0.0.0", "5000"),
        "workers": 4,
    }
    initialize()
    HttpServer(app, options).run()
