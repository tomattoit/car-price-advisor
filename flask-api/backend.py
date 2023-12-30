from flask import Flask, request, jsonify
from flask_cors import CORS

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import pandas as pd
import pickle
import time

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
MODEL_PICKLE_PATH = "./catboost.pkl"

model = None
last_event_time = None


def init_model():
    global model
    if not os.path.exists(MODEL_PICKLE_PATH):
        model = None
        return
    with open(MODEL_PICKLE_PATH, "rb") as f:
        model = pickle.load(f)


def init_observer():
    observer = Observer()
    event_handler = ModelChangedHandler()
    observer.schedule(
        event_handler, path=os.path.dirname(MODEL_PICKLE_PATH), recursive=False
    )
    observer.start()
    return observer


class ModelChangedHandler(FileSystemEventHandler):
    def _handle_event(self, event):
        global last_event_time
        current_time = time.time()
        if event.src_path == MODEL_PICKLE_PATH and (
            last_event_time is None or current_time - last_event_time > 1
        ):
            last_event_time = current_time
            print("Model changed, reloading...")
            init_model()

    def on_modified(self, event):
        self._handle_event(event)

    def on_created(self, event):
        self._handle_event(event)

    def on_deleted(self, event):
        self._handle_event(event)


@app.route("/api/predict", methods=["POST"])
def predict_endpoint():
    if not model:
        return {"error": "Model not initialized"}, 500
    data = pd.json_normalize(request.json)[FEATURES]
    prediction = model.predict(data)[0]
    return jsonify(prediction)


def start_program(is_local_server):
    observer = None
    try:
        init_model()
        observer = init_observer()
        if is_local_server:
            app.run(debug=True)
    finally:
        if observer:
            observer.stop()
        if observer:
            observer.join()


start_program(__name__ == "__main__")
