import os
import random

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
import threading
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from model.DbAccess import DBAccess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' # Change this in a real app!
socketio = SocketIO(app, manage_session=True, cors_allowed_origins="*")  # Enable CORS for all origins
app.secret_key = os.urandom(24)  # New key on each restart

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

db = DBAccess()

# Flask-Login user loader
from model.User import User
@login_manager.user_loader
def load_user(user_id):
    # Flask-Login needs this to reload the user from session
    user = db.get_user_by_id(user_id)
    return user







@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirect to login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.get_user_by_username(username)

        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('chat_index'))  # Redirect to chat page
        else:
            flash('Invalid username or password', 'error')


    return render_template('Index.html')


@app.route('/chat')
@login_required
def chat_index():
    return render_template('chat/Index.html') # create index.html



#WebSocket events




@socketio.on('connect')
def handle_connect():
    print(f'[SocketIO] Authenticated? {current_user.is_authenticated}')
    if current_user.is_authenticated:
        print(f'[SocketIO] Connected user: {current_user.username}, ID: {current_user.id}')
        emit('client_connected', {
            'data': f'Connected! Your user ID is {current_user.id}',
            'user_id': current_user.id,
            'username': current_user.username
        })
    else:
        print('[SocketIO] Unauthenticated user tried to connect.')
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    print(f'User {current_user.get_id()} disconnected, logging out')
    logout_user()


@socketio.on('client_send_message')  # Define a custom event
def handle_message(data):
    print('received message from client: ' + str(data))
    emit('server_received_client_message', {'data': data['data'], 'user_id': data['userid'], 'username': data['username']},broadcast=True)





host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
port = int(os.environ.get('FLASK_RUN_PORT', 5000))

if __name__ == '__main__':
    socketio.run(app,
                    host=host,
                    port=port,
                    debug=True)