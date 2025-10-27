import json
import os
from flask import Flask, request, jsonify


app = Flask(__name__)

#data.json placering
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    # Læs eksiterende liste eller lav ny hvis der ikke findes en i forvejen.
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    #Funktion der gemmer dataen i JSON filen.
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/data", methods=["POST"])
def receive_data():
    new_data = request.get_json(silent=True)
    if not new_data:
        return jsonify({"error": "No data received"}), 400

    all_data = load_data()
    all_data.append(new_data)
    save_data(all_data)

    return jsonify({"status": "saved"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    #Return alt data der er gemt i json filen.
    return jsonify(load_data())