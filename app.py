from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def get_user_id_from_username(username: str):
    url = "https://users.roblox.com/v1/usernames/users"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    data = {
        "usernames": [username],
        "excludeBannedUsers": False
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        try:
            user_id = response.json()['data'][0]['id']
            return user_id
        except (KeyError, IndexError):
            return None
    else:
        return None

def get_universe_id_from_place_id(place_id: int):
    url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            universe_id = response.json()['universeId']
            return universe_id
        except (KeyError):
            return None
    else:
        return None

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/api/v1/getuseridfromusername', methods=['GET'])
def get_user_id_route():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400

    user_id = get_user_id_from_username(username)
    if user_id is not None:
        return jsonify({"user_id": user_id})
    else:
        return jsonify({"error": "User not found or an error occurred"}), 404

@app.route('/api/v1/getuniverseidfromplaceid', methods=['GET'])
def get_universe_id_route():
    place_id = request.args.get('placeid')
    if not place_id:
        return jsonify({"error": "Place ID parameter is required"}), 400

    try:
        place_id = int(place_id)
    except ValueError:
        return jsonify({"error": "Place ID must be an integer"}), 400

    universe_id = get_universe_id_from_place_id(place_id)
    if universe_id is not None:
        return jsonify({"universe_id": universe_id})
    else:
        return jsonify({"error": "Place not found or an error occurred"}), 404

if __name__ == '__main__':
    app.run(port=5000)
