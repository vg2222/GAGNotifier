from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

RARE_EGGS = {"Mythical Egg", "Bug Egg"}
RARE_HONEYEVENT = {
    "Nectarine", "Honey Sprinkler", "Bee Egg"
}

@app.route("/")
def index():
    try:
        response = requests.get("https://www.gamersberg.com/api/grow-a-garden/stock")
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("success") and json_data["data"]:
                data = json_data["data"][0]

                player = data.get("playerName", "Unknown Player")
                weather = data.get("weather", {}).get("type", "")
                beanstalk = data.get("seeds", {}).get("Beanstalk", "0")
                gear = data.get("gear", {})
                honeyevent = data.get("honeyevent", {})
                eggs = data.get("eggs", [])

                notify_reasons = []

                if weather == "Thunderstorm":
                    notify_reasons.append("⛈️ Thunderstorm")

                if beanstalk and int(beanstalk) > 0:
                    notify_reasons.append(f"🌱 Beanstalk: {beanstalk}")

                rare_eggs_found = [egg for egg in eggs if egg["name"] in RARE_EGGS and egg["quantity"] > 0]
                if rare_eggs_found:
                    egg_str = ", ".join(f"{egg['name']}: {egg['quantity']}" for egg in rare_eggs_found)
                    notify_reasons.append(f"🥚 Rare Eggs - {egg_str}")

                if gear.get("Master Sprinkler") and int(gear["Master Sprinkler"]) > 0:
                    notify_reasons.append(f"🚿 Master Sprinkler: {gear['Master Sprinkler']}")

                rare_honey = [name for name, qty in honeyevent.items() if name in RARE_HONEYEVENT and int(qty) > 0]
                if rare_honey:
                    honey_str = ", ".join(rare_honey)
                    notify_reasons.append(f"🍯 HoneyEvent Items - {honey_str}")

                return jsonify({
                    "player": player,
                    "alerts": notify_reasons
                })
            else:
                return jsonify({"error": "No data"}), 404
        else:
            return jsonify({"error": f"HTTP {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
