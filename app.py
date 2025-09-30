from flask import Flask, render_template
from flask_socketio import SocketIO, send
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# --- DB functions ---
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL
                )""")
    conn.commit()
    conn.close()

def save_message(msg):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (text) VALUES (?)", (msg,))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("SELECT text FROM messages")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

# --- Routes ---
@app.route("/")
def chat():
    return render_template("chat.html")

# --- Socket.IO events ---
@socketio.on("connect")
def handle_connect():
    # Send history on connect
    for msg in get_all_messages():
        send(msg)

@socketio.on("message")
def handle_message(msg):
    save_message(msg)
    send(msg, broadcast=True)

if __name__ == "__main__":
    init_db()
    socketio.run(app, host="0.0.0.0", port=5000)
