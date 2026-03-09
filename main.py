from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DB_FILE = "users.json"

# פונקציה לטעינת הנתונים מהקובץ
def load_data():
    if not os.path.exists(DB_FILE):
        # אם הקובץ לא קיים, ניצור מבנה ריק
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# פונקציה לשמירת הנתונים לקובץ
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return "Cookie Israel Server is Online!"

# נתיב להרשמה (REGISTER)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = data.get("username")
    pwd = data.get("password")
    
    if not user or not pwd:
        return jsonify({"status": "error", "message": "Missing fields"}), 400
    
    db = load_data()
    if user in db:
        return jsonify({"status": "error", "message": "User already exists"}), 400
    
    # יצירת משתמש חדש עם 0 עוגיות
    db[user] = {"password": pwd, "cookies": 0}
    save_data(db)
    return jsonify({"status": "success", "cookies": 0})

# נתיב להתחברות (LOGIN)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = data.get("username")
    pwd = data.get("password")
    
    db = load_data()
    if user in db and db[user]["password"] == pwd:
        return jsonify({"status": "success", "cookies": db[user]["cookies"]})
    
    return jsonify({"status": "error", "message": "Invalid username or password"}), 401

# נתיב לשמירת נתונים (SAVE)
@app.route('/save', methods=['POST'])
def save():
    data = request.json
    user = data.get("username")
    pwd = data.get("password")
    cookies = data.get("cookies")
    
    db = load_data()
    # אימות שהמשתמש והסיסמה נכונים לפני השמירה
    if user in db and db[user]["password"] == pwd:
        db[user]["cookies"] = cookies
        save_data(db)
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": "Auth failed"}), 401

if __name__ == "__main__":
    # Render משתמש בפורט 10000 בדרך כלל
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
