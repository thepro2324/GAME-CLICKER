from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DB_FILE = "users.json"

def load_data():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

@app.route('/')
def home(): return "Cookie Server Online"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user, pwd = data.get("username"), data.get("password")
    db = load_data()
    if user in db and db[user]["password"] == pwd:
        return jsonify({"status": "success", "cookies": db[user]["cookies"]})
    return jsonify({"status": "error"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user, pwd = data.get("username"), data.get("password")
    db = load_data()
    if user in db: return jsonify({"status": "error"}), 400
    db[user] = {"password": pwd, "cookies": 0}
    save_data(db)
    return jsonify({"status": "success", "cookies": 0})

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    user, pwd, cookies = data.get("username"), data.get("password"), data.get("cookies")
    db = load_data()
    if user in db and db[user]["password"] == pwd:
        db[user]["cookies"] = cookies
        save_data(db)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
