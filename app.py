from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Création de la base de données SQLite
def init_db():
    conn = sqlite3.connect("pda_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pda_usage (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pda_id TEXT NOT NULL,
                        user_name TEXT NOT NULL,
                        status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Route pour afficher l'interface web
@app.route('/')
def index():
    return render_template("index.html")

# Route pour récupérer la liste des PDA et leur statut
@app.route('/get_pda', methods=['GET'])
def get_pda():
    conn = sqlite3.connect("pda_tracking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pda_usage")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# Route pour attribuer un PDA
@app.route('/assign_pda', methods=['POST'])
def assign_pda():
    data = request.json
    pda_id = data['pda_id']
    user_name = data['user_name']
    
    conn = sqlite3.connect("pda_tracking.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pda_usage (pda_id, user_name, status) VALUES (?, ?, ?)", (pda_id, user_name, "Assigned"))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "PDA attribué avec succès!"})

# Route pour retourner un PDA
@app.route('/return_pda', methods=['POST'])
def return_pda():
    data = request.json
    pda_id = data['pda_id']
    
    conn = sqlite3.connect("pda_tracking.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pda_usage WHERE pda_id = ?", (pda_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "PDA retourné avec succès!"})

if __name__ == '__main__':
    app.run(debug=True)


