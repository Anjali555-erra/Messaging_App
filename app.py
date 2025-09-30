from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store messages in memory (clears only if server restarts or redeploys)
chat_history = []

@app.route("/")
def chat():
    return render_template("chat.html")

@socketio.on("connect")
def handle_connect():
    # Send chat history when a new user connects
    for msg in chat_history:
        send(msg)

@socketio.on("message")
def handle_message(msg):
    chat_history.append(msg)  # save message
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
