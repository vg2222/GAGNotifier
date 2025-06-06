from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__, static_folder='static', template_folder='static')

RARE_HONEYEVENT = {"Nectarine", "Honey Sprinkler", "Bee Egg"}

def fetch_data():
    try:
        response = requests.get("https://www.gamersberg.com/api/grow-a-garden/stock")
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("success") and json_data["data"]:
                result = []
                for garden in json_data["data"]:
                    honeyevent = garden.get("honeyevent", {})
                    rare_items = {
                        name: int(qty) for name, qty in honeyevent.items()
                        if name in RARE_HONEYEVENT and int(qty) > 0
                    }
                    if rare_items:
                        result.append({
                            "player": garden.get("playerName", "Unknown Player"),
                            "items": rare_items
                        })
                return result
    except Exception as e:
        print(f"[ERROR] {e}")
    return []

@app.route("/api/data")
def api():
    return jsonify(fetch_data())

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
