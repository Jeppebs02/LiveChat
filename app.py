import os
import random

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' # Change this in a real app!
socketio = SocketIO(app)

user_counter = 0
counter_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html') # create index.html

@socketio.on('connect')
def handle_connect():
    global user_counter
    with counter_lock:
        user_id = user_counter
        user_counter += 1

    print(f'Client connected with User ID: {user_id}')
    emit('client_connected', {
                                        'data': f'Connected! Your user ID is {user_id}',
                                        'user_id': user_id})  # Send the user ID back to the client

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('client_send_message')  # Define a custom event
def handle_message(data):
    print('received message from client: ' + str(data))
    emit('server_received_client_message', {'data': data['data'], 'user_id': data['userid']},broadcast=True)





host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
port = int(os.environ.get('FLASK_RUN_PORT', 5000))

if __name__ == '__main__':
    socketio.run(app,
                    host=host,
                    port=port,
                    debug=True)