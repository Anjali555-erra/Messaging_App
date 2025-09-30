from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'  # change this if you want
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("chat.html")

@socketio.on("message")
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)  # send to all clients

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
